#!/usr/bin/env python3
import sys
from pathlib import Path
import re
import pdfplumber

# Mocking or importing functions from the original script
from crea_tabella_aggiornamento_articoli import (
    _estrai_codice, 
    _descrizione_minima, 
    CONSOLIDAMENTO, 
    _estrai_porzioni_per_unita,
    _raccogli_dati_da_pdf
)

def run_simulation():
    print("Inizio simulazione estrazione articoli dai PDF più recenti...")
    
    # Esegui la raccolta dati (usa la logica originale del script)
    dati = _raccogli_dati_da_pdf()
    
    if not dati:
        print("ERRORE: Nessun dato estratto dai PDF.")
        return

    print(f"Righe grezze estratte dai PDF: {len(dati)}")
    
    by_codice = {}
    for cell0, cell1, cell5 in dati:
        cod = _estrai_codice(cell0)
        if not cod or not re.search(r"[A-Z0-9]{2,}-[A-Z0-9\-]+", cod):
            continue
        desc = _descrizione_minima(cell1)
        conf = (cell5 or "").strip()
        
        # Salviamo anche l'originale per verifica
        if cod not in by_codice or len(desc) > len(by_codice[cod]['desc']):
            by_codice[cod] = {
                'desc': desc,
                'conf_raw': cell5,
                'conf_pulito': conf
            }

    print(f"Articoli univoci trovati: {len(by_codice)}")
    print("\nVerifica caratteristiche di scrittura:")
    print("-" * 120)
    print(f"{'Codice':<20} | {'Descrizione (Normalizzata)':<45} | {'Porz/Unità':<15} | {'Originale Confezionamento'}")
    print("-" * 120)
    
    for cod in sorted(by_codice.keys()):
        info = by_codice[cod]
        desc = info['desc']
        conf_raw = info['conf_raw']
        
        porz_unita = ""
        if cod in CONSOLIDAMENTO:
            up, us, r = CONSOLIDAMENTO[cod]
            porz_unita = f"{r} {us}/{up}"
        else:
            porz_unita = _estrai_porzioni_per_unita(info['conf_pulito'])
            if cod == "10-GEL" and not porz_unita:
                porz_unita = "1"
        
        print(f"{cod:<20} | {desc[:42]:<45} | {porz_unita:<15} | {str(conf_raw).replace('\n', ' ')}")

if __name__ == "__main__":
    run_simulation()
