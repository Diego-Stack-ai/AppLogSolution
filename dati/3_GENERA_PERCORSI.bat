@echo off
setlocal
cd /d "%~dp0"

echo ---------------------------------------------------------
echo   GENERAZIONE PERCORSI OTTIMIZZATI (VEGGIANO)
echo ---------------------------------------------------------
echo.
echo Sto analizzando i giri salvati...
echo.

python "PROGRAMMA\6_genera_percorsi_veggiano.py"

echo.
echo ---------------------------------------------------------
echo OPERAZIONE COMPLETATA!
echo I file sono nella cartella CONSEGNE/CONSEGNE_[DATA]/PERCORSI_VEGGIANO/
echo ---------------------------------------------------------
echo.
pause
