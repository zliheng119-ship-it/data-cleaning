from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import struct

import numpy as np
import pandas as pd


RAW_SUFFIXES = {".cex", ".nda", ".ndax"}
CEX_RECORD_LENGTH = 16

# Calibrated from a LAND CEX file and its official exported workbook.
CEX_VOLTAGE_SCALE = 0.00015500992087494875
CEX_CURRENT_SCALE = 0.00031001977136355426


@dataclass(frozen=True)
class CexRecord:
    offset: int
    time_ms: int
    voltage_raw: int
    current_raw: int
    capacity_ah: float
    energy_wh: float


def read_cex_record(data: bytes, offset: int) -> CexRecord:
    time_ms = struct.unpack_from("<I", data, offset)[0]
    voltage_raw, current_raw = struct.unpack_from("<hh", data, offset + 4)
    capacity_ah, energy_wh = struct.unpack_from("<ff", data, offset + 8)
    return CexRecord(
        offset=offset,
        time_ms=time_ms,
        voltage_raw=voltage_raw,
        current_raw=current_raw,
        capacity_ah=capacity_ah,
        energy_wh=energy_wh,
    )


def is_valid_cex_record(record: CexRecord) -> bool:
    rest_current = abs(record.current_raw) <= 10
    constant_current = 1_000 <= abs(record.current_raw) <= 10_000
    return (
        0 <= record.time_ms < 1_000_000_000
        and 500 <= record.voltage_raw <= 20_000
        and -20_000 <= record.current_raw <= 20_000
        and (rest_current or constant_current)
        and np.isfinite(record.capacity_ah)
        and np.isfinite(record.energy_wh)
        and 0 <= record.capacity_ah < 100
        and 0 <= record.energy_wh < 100
    )


def step_type(current_ma: float) -> str:
    if abs(current_ma) <= 1e-9:
        return "rest"
    if current_ma > 0:
        return "charge"
    return "discharge"


def parse_cex(path: Path) -> pd.DataFrame:
    data = path.read_bytes()
    rows: list[dict] = []
    record_index = 0
    step_index = 0
    cycle = 0
    previous_step_type: str | None = None
    previous_capacity: float | None = None

    for offset in range(0, len(data) - CEX_RECORD_LENGTH + 1, CEX_RECORD_LENGTH):
        record = read_cex_record(data, offset)
        if not is_valid_cex_record(record):
            continue

        voltage_v = record.voltage_raw * CEX_VOLTAGE_SCALE
        current_ma = record.current_raw * CEX_CURRENT_SCALE
        capacity_mah = record.capacity_ah * 1000
        current_step_type = step_type(current_ma)
        capacity_reset = (
            previous_capacity is not None
            and capacity_mah + 1e-6 < previous_capacity
            and capacity_mah < 1
        )
        new_step = (
            previous_step_type is None
            or current_step_type != previous_step_type
            or capacity_reset
        )
        if new_step:
            step_index += 1
            point_in_step = 1
            if current_step_type == "discharge":
                cycle += 1
        else:
            point_in_step = int(rows[-1]["point_in_step"]) + 1

        record_index += 1
        rows.append(
            {
                "record_index": record_index,
                "cycle": cycle if cycle > 0 else pd.NA,
                "step_index": step_index,
                "step_type": current_step_type,
                "point_in_step": point_in_step,
                "time_s": record.time_ms / 1000,
                "voltage_v": voltage_v,
                "current_ma": current_ma,
                "capacity_mah": capacity_mah,
                "energy_mwh": record.energy_wh * 1000,
                "source_offset": record.offset,
            }
        )
        previous_step_type = current_step_type
        previous_capacity = capacity_mah

    if not rows:
        raise ValueError(f"No valid CEX data records were parsed from: {path}")
    return pd.DataFrame(rows)


def parse_nda(path: Path) -> pd.DataFrame:
    try:
        import NewareNDA
    except ImportError as exc:
        raise ImportError(
            "Parsing .nda/.ndax files requires NewareNDA. Run: python -m pip install NewareNDA"
        ) from exc

    raw = NewareNDA.read(str(path))
    required = [
        "Index",
        "Cycle",
        "Step",
        "Status",
        "Time",
        "Voltage",
        "Current(mA)",
        "Charge_Capacity(mAh)",
        "Discharge_Capacity(mAh)",
        "Charge_Energy(mWh)",
        "Discharge_Energy(mWh)",
    ]
    missing = [column for column in required if column not in raw.columns]
    if missing:
        raise ValueError(f"NDA/NDAX file is missing columns: {', '.join(missing)}")

    df = raw.copy()
    status_map = {
        "Rest": "rest",
        "CC_Chg": "charge",
        "CC_DChg": "discharge",
        "CV_Chg": "charge",
        "CV_DChg": "discharge",
    }
    df["step_type"] = df["Status"].map(status_map).fillna(df["Status"].astype(str))
    df["capacity_mah"] = np.select(
        [df["step_type"].eq("charge"), df["step_type"].eq("discharge")],
        [df["Charge_Capacity(mAh)"], df["Discharge_Capacity(mAh)"]],
        default=0,
    )
    df["energy_mwh"] = np.select(
        [df["step_type"].eq("charge"), df["step_type"].eq("discharge")],
        [df["Charge_Energy(mWh)"], df["Discharge_Energy(mWh)"]],
        default=0,
    )

    result = pd.DataFrame(
        {
            "record_index": pd.to_numeric(df["Index"], errors="coerce").astype("Int64"),
            "cycle": pd.to_numeric(df["Cycle"], errors="coerce").astype("Int64"),
            "step_index": pd.to_numeric(df["Step"], errors="coerce").astype("Int64"),
            "step_type": df["step_type"],
            "point_in_step": df.groupby("Step").cumcount() + 1,
            "time_s": pd.to_numeric(df["Time"], errors="coerce"),
            "voltage_v": pd.to_numeric(df["Voltage"], errors="coerce"),
            "current_ma": pd.to_numeric(df["Current(mA)"], errors="coerce"),
            "capacity_mah": pd.to_numeric(df["capacity_mah"], errors="coerce"),
            "energy_mwh": pd.to_numeric(df["energy_mwh"], errors="coerce"),
            "source_offset": pd.NA,
        }
    )
    if "Timestamp" in df.columns:
        result["timestamp"] = df["Timestamp"].astype(str)

    result = result.dropna(subset=["record_index", "cycle", "step_index", "time_s", "voltage_v"])
    if result.empty:
        raise ValueError(f"No valid NDA/NDAX data records were parsed from: {path}")
    return result.sort_values("record_index").reset_index(drop=True)


def parse_raw_file(path: Path) -> pd.DataFrame:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".cex":
        return parse_cex(path)
    if suffix in {".nda", ".ndax"}:
        return parse_nda(path)
    raise ValueError(f"Unsupported input file type: {path.suffix}")

