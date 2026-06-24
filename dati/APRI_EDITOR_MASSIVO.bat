@echo off
title Editor Massivo Excel
cd /d "%~dp0PROGRAMMA"
echo Avvio dell'Editor Massivo...
python 5_editor_massivo_excel.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo Si e' verificato un errore durante l'avvio.
    echo Assicurati di aver installato le librerie necessarie:
    echo pip install pandas openpyxl flask
    pause
)
pause
