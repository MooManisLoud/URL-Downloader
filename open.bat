@echo off

REM Check if Python is installed
python --version 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python from https://www.python.org/downloads/ and try again.
    pause
    exit /b
)

REM Check if required Python packages are installed
python -c "import tkinter" 2>nul
if %errorlevel% neq 0 (
    echo Required Python package 'tkinter' is not installed. Installing...
    python -m pip install tkinter
)

python -c "import requests" 2>nul
if %errorlevel% neq 0 (
    echo Required Python package 'requests' is not installed. Installing...
    python -m pip install requests
)

python -c "import PIL" 2>nul
if %errorlevel% neq 0 (
    echo Required Python package 'Pillow' is not installed. Installing...
    python -m pip install pillow
)

REM Run the Python script
python3 URLDownloader.py
