@echo off
echo Launching Fake Review Detection System...
cd /d "%~dp0"
streamlit run app.py
pause