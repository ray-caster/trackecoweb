@echo off
REM Setup script for daily statistics update on Windows
REM This sets up a Windows Task Scheduler task to run daily at 8 PM WIB

set SCRIPT_DIR=%~dp0
set PYTHON_SCRIPT=%SCRIPT_DIR%daily_update.py

REM Find Python executable
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PYTHON_PATH=python
) else (
    where python3 >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_PATH=python3
    ) else (
        echo Error: Python not found in PATH
        exit /b 1
    )
)

REM Delete existing task if it exists
schtasks /Delete /TN "TrackEco_DailyUpdate" /F >nul 2>nul

REM Create new scheduled task (8 PM WIB)
schtasks /Create /TN "TrackEco_DailyUpdate" /TR "%PYTHON_PATH% %PYTHON_SCRIPT%" /SC DAILY /ST 20:00 /F

if %ERRORLEVEL% EQU 0 (
    echo ✓ Daily update task has been set up successfully!
    echo   Schedule: Every day at 8:00 PM WIB
    echo   Script: %PYTHON_SCRIPT%
    echo.
    echo To verify the task, run: schtasks /Query /TN "TrackEco_DailyUpdate"
    echo To remove the task, run: schtasks /Delete /TN "TrackEco_DailyUpdate" /F
) else (
    echo ✗ Failed to create scheduled task
    echo   Please run this script as Administrator
)

pause

