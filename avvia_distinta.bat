@echo off
cd /d "c:\Gestione DDT viaggi"
py -3 Programma\crea_distinta_magazzino.py
py -3 Programma\crea_ddt_originali.py
pause
