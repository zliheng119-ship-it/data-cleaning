from __future__ import annotations

from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from .parsers import parse_raw_file
from .style import apply_matplotlib_style, cm_to_inch, load_style


def timestamp_elapsed_seconds(df: pd.DataFrame) -> pd.Series | None:
    if "timestamp" not in df.columns:
        return None
    timestamp = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    if timestamp.notna().sum() < 2:
        return None
    start = timestamp.dropna().iloc[0]
    elapsed = (timestamp - start).dt.total_seconds()
    if elapsed.notna().sum() < 2:
        return None
    return elapsed


def prepare_voltage_time_data(df: pd.DataFrame, time_unit: str = "h") -> pd.DataFrame:
    if time_unit not in {"s", "min", "h"}:
        raise ValueError("time_unit must be one of: s, min, h")

    required = ["record_index", "time_s", "voltage_v"]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Parsed table is missing columns: {', '.join(missing)}")

    factor = {"s": 1.0, "min": 60.0, "h": 3600.0}[time_unit]
    plot_df = df.sort_values("record_index").copy()
    seconds = timestamp_elapsed_seconds(plot_df)
    if seconds is None:
        seconds = pd.to_numeric(plot_df["time_s"], errors="coerce")

    plot_df["time_h"] = (seconds - seconds.iloc[0]) / 3600.0
    plot_df[f"time_{time_unit}"] = (seconds - seconds.iloc[0]) / factor
    plot_df["voltage_v"] = pd.to_numeric(plot_df["voltage_v"], errors="coerce")
    plot_df["current_ma"] = pd.to_numeric(plot_df.get("current_ma"), errors="coerce")
    plot_df = plot_df.dropna(subset=[f"time_{time_unit}", "voltage_v"])
    if plot_df.empty:
        raise ValueError("No valid voltage-time data is available for plotting.")

    columns = [
        "record_index",
        "cycle",
        "step_index",
        "step_type",
        f"time_{time_unit}",
        "time_h",
        "voltage_v",
        "current_ma",
        "capacity_mah",
        "energy_mwh",
    ]
    existing_columns = [column for column in columns if column in plot_df.columns]
    return plot_df[existing_columns].reset_index(drop=True)


def plot_voltage_time(
    input_path: Path,
    output_dir: Path | None = None,
    style_path: Path | None = None,
    time_unit: str = "h",
) -> dict[str, Path]:
    input_path = Path(input_path).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    output_dir = Path(output_dir).resolve() if output_dir is not None else input_path.parent / f"{input_path.stem}_voltage_time"
    output_dir.mkdir(parents=True, exist_ok=True)

    parsed = parse_raw_file(input_path)
    data = prepare_voltage_time_data(parsed, time_unit=time_unit)
    data_path = output_dir / f"{input_path.stem}_voltage_time_data.xlsx"
    with pd.ExcelWriter(data_path, engine="openpyxl") as writer:
        data.to_excel(writer, sheet_name="voltage_time", index=False)

    style = load_style(style_path)
    apply_matplotlib_style(style)
    active_time_unit = time_unit or style.get("time_unit", "h")
    time_column = f"time_{active_time_unit}"
    if time_column not in data.columns:
        data = prepare_voltage_time_data(parsed, time_unit=active_time_unit)

    fig, ax = plt.subplots(
        figsize=(
            cm_to_inch(float(style.get("figure_width_cm", 11.0))),
            cm_to_inch(float(style.get("figure_height_cm", 6.0))),
        )
    )
    colors = style.get("colors", ["#000000"])
    ax.plot(
        data[time_column],
        data["voltage_v"],
        color=colors[0],
        linewidth=float(style.get("line_width", 1.4)),
        alpha=float(style.get("line_alpha", 0.95)),
    )
    ax.set_xlabel(style.get("xlabel", f"Time ({active_time_unit})"))
    ax.set_ylabel(style.get("ylabel", "Voltage (V)"))
    ax.tick_params(
        direction=style.get("tick_direction", "out"),
        width=float(style.get("tick_width", 1.2)),
        length=float(style.get("tick_length", 4)),
    )
    if style.get("xlim") is not None:
        ax.set_xlim(style["xlim"])
    if style.get("ylim") is not None:
        ax.set_ylim(style["ylim"])

    svg_path = output_dir / "plot.svg"
    fig.savefig(svg_path, bbox_inches="tight")
    plt.close(fig)
    return {"data": data_path, "svg": svg_path}

