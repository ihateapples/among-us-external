@echo off
cd /d "%~dp0"

pip install --upgrade pyinstaller

pyinstaller ^
 --onefile ^
 --noconsole ^
 --icon=loading.ico ^
 --add-data "loading.png;." ^
 main.py

pause
