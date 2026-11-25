@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe py -m venv .venv || goto :error
.venv\Scripts\python.exe -m pip install -r requirements.txt || goto :error
.venv\Scripts\python.exe -m unittest discover -s . -p test_engine.py -v || goto :error
.venv\Scripts\python.exe audit_data.py || goto :error
.venv\Scripts\python.exe generate_outputs.py || goto :error
.venv\Scripts\python.exe -m streamlit run app.py || goto :error
exit /b 0
:error
echo A step failed. Read the error and README.md.
pause
exit /b 1
