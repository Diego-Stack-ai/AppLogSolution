@echo off
chcp 65001 >nul
title AGGIORNA TEMPI TRAFFICO (10:00-13:00)
echo.
echo  ============================================
echo   AGGIORNAMENTO CACHE TRAFFICO MULTI-ORARIO
echo   Fasce: 10:00 / 10:30 / 11:00 / 11:30
echo          12:00 / 12:30 / 13:00
echo   Da lanciare a fine giornata o la mattina
echo  ============================================
echo.
cd /d "%~dp0PROGRAMMA"
python aggiorna_traffico_serale.py
echo.
pause
