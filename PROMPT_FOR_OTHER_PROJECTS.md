# Prompt For Other Projects

Copy the prompt below into another project's AI assistant conversation, or put
it in that project's `AGENTS.md` or `README.md`.

```text
This project can call a local battery data processing toolkit located at:
battery-data-toolkit

When I need to process .cex, .nda, or .ndax raw battery data and plot a
voltage-time curve, use this toolkit first instead of rewriting a new script.

How to call it:

1. Enter the battery-data-toolkit directory.
2. If .venv\Scripts\python.exe exists, prefer it.
3. Run:

   .venv\Scripts\python.exe -m battery_data_tool voltage-time --input "<input_file>" --output-dir "<output_dir>" --time-unit h

   If no local .venv exists, run:

   python -m battery_data_tool voltage-time --input "<input_file>" --output-dir "<output_dir>" --time-unit h

4. The output should contain:
   - plot.svg
   - *_voltage_time_data.xlsx

5. Do not modify raw input files. Put outputs in the current project's result
   folder, not inside the toolkit source directory.

If dependencies are missing, run install_dependencies.bat in the
battery-data-toolkit directory first.
```
