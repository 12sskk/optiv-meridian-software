@echo off
echo =========================================================================
echo Optiv TPRM ^| Meridian Financial AI Due Diligence Platform
echo =========================================================================
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Setting up Python virtual environment...
    py -3.12 -m venv .venv || py -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

echo [INFO] Launching Streamlit Application...
streamlit run app.py
pause
