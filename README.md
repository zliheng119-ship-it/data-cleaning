# Battery Data Toolkit

This is a portable local toolkit for battery data processing. Copy the whole
`battery-data-toolkit` folder into another project and run it there.

## Current Features

```text
.cex/.nda/.ndax -> voltage-time curve
```

Current outputs:

```text
plot.svg
<input_stem>_voltage_time_data.xlsx
```

## First-Time Setup

Double-click:

```text
install_dependencies.bat
```

This creates a local `.venv` folder inside the toolkit and installs:

```text
pandas
numpy
matplotlib
openpyxl
NewareNDA
```

## Plot Voltage-Time Curve

The simplest way:

```text
Drag a .cex/.nda/.ndax file onto plot_voltage_time.bat
```

Command-line usage:

```bat
python -m battery_data_tool voltage-time --input "D:\project\data.ndax" --output-dir "D:\project\result" --time-unit h
```

## Output Location

If no output folder is provided, the toolkit creates a folder next to the input
file:

```text
<input_stem>_voltage_time_output
```

The folder contains:

```text
plot.svg
<input_stem>_voltage_time_data.xlsx
```

## Plot Style

The default style template is:

```text
templates\voltage_time_style.json
```

You can edit the font, font size, axis line width, tick width, line width,
figure size, axis limits, and colors there.
