@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

set "BASE_DIR=%~dp0"
if "%BASE_DIR:~-1%"=="\" set "BASE_DIR=%BASE_DIR:~0,-1%"

echo ===========================================
echo   AVVIO PROCEDURA CONSEGNE
echo ===========================================
echo Cartella base: "%BASE_DIR%"

:: 1. Controllo Python
echo [1/4] Controllo Python...
set "PYTHON_EXE="
where python >nul 2>nul
if %ERRORLEVEL%==0 (
    set "PYTHON_EXE=python"
) else (
    where py >nul 2>nul
    if %ERRORLEVEL%==0 set "PYTHON_EXE=py -3"
)

if not defined PYTHON_EXE (
    echo [ERRORE] Python non trovato. Installa Python 3.
    pause
    exit /b 1
)

:: 2. Controllo venv
set "VENV_DIR=%BASE_DIR%\venv"
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [2/4] Creazione ambiente virtuale (venv)...
    "%PYTHON_EXE%" -m venv "%VENV_DIR%"
    if %ERRORLEVEL% NEQ 0 (
        echo [ERRORE] Impossibile creare venv.
        pause
        exit /b 1
    )
    echo Installazione librerie...
    "%VENV_DIR%\Scripts\pip.exe" install -r "%BASE_DIR%\requirements.txt"
) else (
    echo [2/4] Ambiente virtuale gia' presente.
)

:: 3. Esecuzione Script
set PY_EXE="%VENV_DIR%\Scripts\python.exe"
set "DATA_ARG=%~1"

echo.
echo [3/4] Esecuzione Script in sequenza...

echo -> 1. Estrazione...
%PY_EXE% "%BASE_DIR%\1_estrai_ddt_consegne.py" %DATA_ARG%
if %ERRORLEVEL% NEQ 0 goto :errore

echo -> 2. Punti Consegna...
%PY_EXE% "%BASE_DIR%\2_crea_punti_consegna.py" %DATA_ARG%
if %ERRORLEVEL% NEQ 0 goto :errore

echo -> 3. Unificazione...
%PY_EXE% "%BASE_DIR%\3_crea_lista_unificata.py" %DATA_ARG%
if %ERRORLEVEL% NEQ 0 goto :errore

echo -> 4. Mappa e App...
%PY_EXE% "%BASE_DIR%\4_crea_mappa_consegne.py" %DATA_ARG%
if %ERRORLEVEL% NEQ 0 goto :errore

echo.
echo ===========================================
echo   ELABORAZIONE COMPLETA CON SUCCESSO
echo ===========================================
pause
exit /b 0

:errore
echo.
echo [ERRORE] Uno degli script ha interrotto l'esecuzione.
pause
exit /b 1
