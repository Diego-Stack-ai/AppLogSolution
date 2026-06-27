@echo off
setlocal
set PYTHONIOENCODING=utf-8
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
echo   CONSOLIDAMENTO ORDINE CONSEGNE (OTTIMIZZATO)
echo ---------------------------------------------------------
echo.
echo Analisi file HTML in PERCORSI_VEGGIANO...
echo.

python "PROGRAMMA\8_genera_json_ottimizzato.py"

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERR ERRORE nella generazione del JSON ottimizzato!
    echo L'operazione e' stata interrotta.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ---------------------------------------------------------
echo OPERAZIONE COMPLETATA!
echo I file sono nella cartella CONSEGNE/CONSEGNE_[DATA]/PERCORSI_VEGGIANO/
echo ---------------------------------------------------------
echo.
pause
