Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host "Optiv TPRM | Meridian Financial AI Due Diligence Platform" -ForegroundColor Cyan
Write-Host "=========================================================================" -ForegroundColor Cyan

$VenvPython = ".\.venv\Scripts\python.exe"
$VenvStreamlit = ".\.venv\Scripts\streamlit.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "[INFO] Initializing Python virtual environment..." -ForegroundColor Yellow
    py -3.12 -m venv .venv
    & $VenvPython -m pip install --upgrade pip
    & $VenvPython -m pip install -r requirements.txt
}

Write-Host "[INFO] Launching Streamlit application on http://localhost:8501..." -ForegroundColor Green
& $VenvStreamlit run app.py
