@echo off
title SYNC COORDINATE REALI DA CLOUD
color 0B
chcp 65001 > nul

echo ------------------------------------------------------------
echo    SINCRONIZZAZIONE COORDINATE REALI (AUTISTI)
echo ------------------------------------------------------------
echo.
echo Sto recuperando i dati dal Cloud Firebase...
echo.

python "PROGRAMMA\10_sync_coordinate_da_cloud.py"

echo.
echo ------------------------------------------------------------
echo OPERAZIONE COMPLETATA!
echo I dati reali sono ora nella Colonna T di mappatura_destinazioni.xlsx
echo ------------------------------------------------------------
echo.
pause
