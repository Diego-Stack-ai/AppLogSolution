@echo off
setlocal
cd /d "%~dp0"

echo ---------------------------------------------------------
echo   GENERAZIONE DISTINTE PDF PER IL MAGAZZINO
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
