@echo off
chcp 65001 >nul
title MAPPA PERCORSI INTERATTIVA
echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║     AVVIO MAPPA PERCORSI INTERATTIVA (BAT 3+)   ║
echo  ║  FASE 1: Editing giri  (nessuna API)             ║
echo  ║  FASE 2: Calcolo percorsi  (OR-Tools + Google)   ║
echo  ║  FASE 3: Revisione + ricalcolo parziale          ║
echo  ╚══════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"
python 6b_mappa_percorsi_interattiva.py %*
pause
