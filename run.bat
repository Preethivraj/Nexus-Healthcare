@echo off
cd /d "%~dp0"
echo ============================================================
echo  Starting Healthcare Clinical Triage Assistant (PS01)
echo  Serving at http://localhost:8000
echo ============================================================
if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe app.py
) else (
    python app.py
)
pause
