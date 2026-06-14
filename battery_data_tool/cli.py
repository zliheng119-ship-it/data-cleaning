from __future__ import annotations

import argparse
from pathlib import Path

from .voltage_time import plot_voltage_time


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Battery data processing toolkit.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    voltage_time = subparsers.add_parser("voltage-time", help="Plot voltage versus time from .cex/.nda/.ndax.")
    voltage_time.add_argument("--input", type=Path, required=True, help="Input .cex/.nda/.ndax file.")
    voltage_time.add_argument("--output-dir", type=Path, default=None, help="Output folder. Defaults beside input.")
    voltage_time.add_argument("--style", type=Path, default=None, help="Optional style JSON file.")
    voltage_time.add_argument("--time-unit", choices=["s", "min", "h"], default="h", help="Time axis unit.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "voltage-time":
        outputs = plot_voltage_time(
            input_path=args.input,
            output_dir=args.output_dir,
            style_path=args.style,
            time_unit=args.time_unit,
        )
        print("Finished.")
        print(f"Data table: {outputs['data']}")
        print(f"SVG figure: {outputs['svg']}")


if __name__ == "__main__":
    main()

