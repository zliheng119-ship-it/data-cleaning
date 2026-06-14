from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl


PACKAGE_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = PACKAGE_ROOT / "templates"


def default_voltage_time_style_path() -> Path:
    return TEMPLATE_DIR / "voltage_time_style.json"


def load_style(style_path: Path | None = None) -> dict:
    path = Path(style_path) if style_path is not None else default_voltage_time_style_path()
    if not path.exists():
        raise FileNotFoundError(f"Style template not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def cm_to_inch(value_cm: float) -> float:
    return value_cm / 2.54


def apply_matplotlib_style(style: dict) -> None:
    font = style.get("font", "Arial")
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [font, "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": float(style.get("font_size", 8)),
            "axes.linewidth": float(style.get("axis_line_width", 1.2)),
            "axes.spines.top": bool(style.get("axes_closed", True)),
            "axes.spines.right": bool(style.get("axes_closed", True)),
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "legend.frameon": False,
        }
    )

