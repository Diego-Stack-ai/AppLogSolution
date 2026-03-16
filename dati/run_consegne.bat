@echo off
REM Avvio unico CONSEGNE: controlla Python, venv e poi lancia estrai_ddt_consegne.py

SETLOCAL ENABLEDELAYEDEXPANSION

REM Cartella base (dove si trova questo .bat), assumiamo sia C:\AppLogSolution\CONSEGNE\
set "BASE_DIR=%~dp0"
REM Rimuove eventuale backslash finale doppio
if "%BASE_DIR:~-1%"=="\" set "BASE_DIR=%BASE_DIR:~0,-1%"

echo.
echo === LOGICA 1: CONTROLLI AMBIENTE ===
echo.

REM 1) Controllo che la cartella CONSEGNE esista
if not exist "%BASE_DIR%" (
    echo [ERRORE] Cartella CONSEGNE non trovata in "%BASE_DIR%".
    echo Copia la cartella CONSEGNE in C:\AppLogSolution\ prima di continuare.
    pause
    exit /b 1
)

REM 2) Controllo Python (prima python, poi py)
set "PYTHON_EXE="
where python >nul 2>nul
if %ERRORLEVEL%==0 set "PYTHON_EXE=python"

if not defined PYTHON_EXE (
    where py >nul 2>nul
    if %ERRORLEVEL%==0 set "PYTHON_EXE=py -3"
)

if not defined PYTHON_EXE (
    echo [ERRORE] Python non risulta installato o non e' nel PATH.
    echo Installa Python 3.x e riapri il prompt, poi rilancia questo comando.
    pause
    exit /b 1
)

echo - Python trovato: %PYTHON_EXE%

REM 3) Controllo / creazione venv
set "VENV_DIR=%BASE_DIR%\venv"

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo.
    echo Creazione ambiente virtuale (venv) in:
    echo   "%VENV_DIR%"
    echo Questa operazione potrebbe richiedere qualche minuto solo la prima volta...
    echo.
    %PYTHON_EXE% -m venv "%VENV_DIR%"
    if %ERRORLEVEL% NEQ 0 (
        echo [ERRORE] Creazione venv non riuscita.
        pause
        exit /b 1
    )

    call "%VENV_DIR%\Scripts\activate.bat"

    if exist "%BASE_DIR%\requirements.txt" (
        echo.
        echo Installo le librerie Python da requirements.txt...
        "%VENV_DIR%\Scripts\pip.exe" install -r "%BASE_DIR%\requirements.txt"
        if %ERRORLEVEL% NEQ 0 (
            echo [ERRORE] Installazione librerie non riuscita.
            pause
            exit /b 1
        )
    ) else (
        echo [ATTENZIONE] requirements.txt non trovato in "%BASE_DIR%".
        echo Procedo comunque, ma potresti dover installare manualmente le librerie.
    )
) else (
    echo.
    echo Ambiente venv gia' presente, lo attivo...
    call "%VENV_DIR%\Scripts\activate.bat"
)

echo.
echo === LOGICA 2: ESECUZIONE SCRIPT CONSEGNE ===
echo.

REM Qui puoi passare una data come parametro, es:
REM   run_consegne.bat 16-03-2026

set "DATA_ARG=%~1"

REM Percorso attuale dello script di estrazione (versione che hai ora nel progetto)
set "ESTRAI_SCRIPT=%BASE_DIR%\CONSEGNE_16-03-2026\estrai_ddt_consegne.py"

if not exist "%ESTRAI_SCRIPT%" (
    echo [ERRORE] Script estrai_ddt_consegne.py non trovato in:
    echo   "%ESTRAI_SCRIPT%"
    echo Verifica la posizione dello script e aggiorna ESTRAI_SCRIPT dentro run_consegne.bat.
    pause
    exit /b 1
)

echo Eseguo:
echo   %VENV_DIR%\Scripts\python.exe "%ESTRAI_SCRIPT%" %DATA_ARG%
echo.

"%VENV_DIR%\Scripts\python.exe" "%ESTRAI_SCRIPT%" %DATA_ARG%

echo.
echo Operazione completata. (Codice uscita: %ERRORLEVEL%)
echo.
pause
ENDLOCAL

