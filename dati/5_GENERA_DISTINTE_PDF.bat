@echo off
setlocal
cd /d "%~dp0"

echo ---------------------------------------------------------
echo   FASE 1: CONSOLIDAMENTO ORDINE CONSEGNE (OTTIMIZZATO)
echo ---------------------------------------------------------
echo.
echo Analisi file HTML in PERCORSI_VEGGIANO...
echo.

python "PROGRAMMA\8_genera_json_ottimizzato.py"

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ ERRORE nella generazione del JSON ottimizzato!
    echo L'operazione e' stata interrotta.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ---------------------------------------------------------
echo   FASE 2: GENERAZIONE DISTINTE PDF PER IL MAGAZZINO
echo ---------------------------------------------------------
echo.
echo Creazione fascicoli [Distinta + DDT] in doppia copia...
echo.

python "PROGRAMMA\9_genera_distinte_da_viaggi.py"

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ ERRORE nella generazione delle distinte PDF!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ---------------------------------------------------------
echo OPERAZIONE COMPLETATA CON SUCCESSO! ✅
echo.
echo Le distinte sono pronte in:
echo   CONSEGNE\CONSEGNE_[DATA]\DISTINTE_VIAGGIO\
echo.
echo Puoi stampare il file MASTER_DISTINTE_[DATA].pdf
echo ---------------------------------------------------------
echo.
pause
