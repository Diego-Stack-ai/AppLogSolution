@echo off
setlocal
cd /d "%~dp0"
echo ELABORAZIONE DDT IN CORSO...
python "PROGRAMMA\(1_2_3_4)_estrai_ddt_consegne.py"
echo.
echo Operazione completata. 
pause
