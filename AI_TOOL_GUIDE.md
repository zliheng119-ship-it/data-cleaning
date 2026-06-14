# AI Tool Guide

This file tells an AI assistant in another project how to call this local
battery data processing toolkit.

## Toolkit Location

If this folder has been copied into the current project, the toolkit root is:

```text
battery-data-toolkit
```

The assistant should run commands from that directory.

## Available Features

### 1. Plot Voltage-Time Curve

Purpose:

```text
Read .cex/.nda/.ndax raw battery data and export a voltage-time curve.
```

Inputs:

```text
.cex
.nda
.ndax
```

Outputs:

```text
plot.svg
<input_stem>_voltage_time_data.xlsx
```

Default time unit:

```text
h
```

## Recommended Commands

From the `battery-data-toolkit` directory, run:

```bat
python -m battery_data_tool voltage-time --input "<input_file>" --output-dir "<output_dir>" --time-unit h
```

Example:

```bat
python -m battery_data_tool voltage-time --input "D:\project\data.ndax" --output-dir "D:\project\voltage_time_result" --time-unit h
```

If the toolkit already has a local `.venv`, prefer:

```bat
".venv\Scripts\python.exe" -m battery_data_tool voltage-time --input "D:\project\data.ndax" --output-dir "D:\project\voltage_time_result" --time-unit h
```

## First-Time Setup

If dependencies are missing, run this in the toolkit directory:

```bat
install_dependencies.bat
```

or:

```bat
python -m pip install -r requirements.txt
```

## AI Calling Rules

1. Do not modify the raw input data.
2. Do not write generated results into the toolkit source directory; write them
   into the current project's result folder.
3. Check that `plot.svg` and `*_voltage_time_data.xlsx` were generated.
4. If the user does not provide an output directory, create a clear result
   folder next to the raw input file, such as:

```text
<input_stem>_voltage_time_output
```

5. If dependencies such as `NewareNDA`, `matplotlib`, or `pandas` are missing,
   run `install_dependencies.bat` first.

## When To Use This Toolkit

Use this toolkit for requests such as:

```text
plot voltage-time curve
voltage-time curve
process .ndax/.nda/.cex data
export a voltage-time table from battery raw data
```

The first version does not yet support:

```text
charge-discharge capacity-voltage curves
Aurbach coulombic efficiency
CV/LSV/EIS/XRD plots
complex batch figure layout
```
