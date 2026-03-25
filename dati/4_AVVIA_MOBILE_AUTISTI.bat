@echo off
title GENERATORE MAPPE MOBILE - AppLogSolution
color 0B
cls
echo ------------------------------------------------------------
echo     GENERAZIONE MAPPE PER SMARTPHONE (WHATSAPP)
echo ------------------------------------------------------------
echo.
echo Sto generando i percorsi in ordine ottimizzato...
python "%~dp0PROGRAMMA\8_genera_mappe_mobile_autisti.py"
echo.
echo ------------------------------------------------------------
echo OPERAZIONE COMPLETATA!
echo I file sono nella cartella MAPPE_MOBILE_AUTISTI del giorno.
echo ------------------------------------------------------------
echo.
pause
