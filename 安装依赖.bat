@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Please install Python first.
  pause
  exit /b 1
)

if not exist "%SCRIPT_DIR%.venv\Scripts\python.exe" (
  python -m venv "%SCRIPT_DIR%.venv"
  if errorlevel 1 (
    echo Failed to create local Python environment.
    pause
    exit /b 1
  )
)

"%SCRIPT_DIR%.venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 (
  echo Failed to upgrade pip.
  pause
  exit /b 1
)

"%SCRIPT_DIR%.venv\Scripts\python.exe" -m pip install -r "%SCRIPT_DIR%requirements.txt"
if errorlevel 1 (
  echo.
  echo Dependency installation failed.
  pause
  exit /b 1
)

echo.
echo Dependencies installed into this toolkit folder.
pause
