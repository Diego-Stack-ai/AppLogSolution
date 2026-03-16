@echo off
cd /d "%~dp0"
echo Estrazione DDT e creazione struttura CONSEGNE_{data}...
echo.
if "%~1"=="" (
    py -3 Programma\estrai_ddt_consegne.py
) else (
    py -3 Programma\estrai_ddt_consegne.py %1
)
echo.
pause
