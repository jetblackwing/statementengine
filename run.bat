@echo off
REM Bank Statement Engine - Windows Runner
REM ======================================
REM This script sets up the virtual environment and runs the GUI application.

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"

REM Remove trailing backslash
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Check if virtual environment exists
if not exist "%SCRIPT_DIR%\.venv" (
    echo Virtual environment not found. Creating one...
    python -m venv "%SCRIPT_DIR%\.venv"
    if errorlevel 1 (
        echo Failed to create virtual environment. Please ensure Python venv is available.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call "%SCRIPT_DIR%\.venv\Scripts\activate.bat"

REM Check if dependencies are installed
python -c "import customtkinter" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r "%SCRIPT_DIR%\requirements.txt"
    if errorlevel 1 (
        echo Failed to install dependencies.
        pause
        exit /b 1
    )
)

REM Run the application
echo Starting Bank Statement Engine...
python "%SCRIPT_DIR%\launcher.py"

REM Deactivate virtual environment
deactivate