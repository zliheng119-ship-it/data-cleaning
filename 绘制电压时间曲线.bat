@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

if exist "%SCRIPT_DIR%.venv\Scripts\python.exe" (
  set "PY=%SCRIPT_DIR%.venv\Scripts\python.exe"
) else (
  set "PY=python"
)

if "%~1"=="" (
  set /p INPUT_FILE=Please drag a .cex/.nda/.ndax file here, or type the full path: 
) else (
  set "INPUT_FILE=%~1"
)

if "%INPUT_FILE%"=="" (
  echo No input file.
  pause
  exit /b 1
)

if "%~2"=="" (
  for %%F in ("%INPUT_FILE%") do set "OUTPUT_DIR=%%~dpF%%~nF_voltage_time_output"
) else (
  set "OUTPUT_DIR=%~2"
)

"%PY%" -m battery_data_tool voltage-time --input "%INPUT_FILE%" --output-dir "%OUTPUT_DIR%" --time-unit h
if errorlevel 1 (
  echo.
  echo Failed. If this is the first time using the toolkit, run 安装依赖.bat first.
  pause
  exit /b 1
)

echo.
echo Output folder:
echo %OUTPUT_DIR%
pause
