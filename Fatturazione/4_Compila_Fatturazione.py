import os
import pandas as pd
import requests
import datetime as dt
import sys

# CONFIGURAZIONE STRUTTURA
DRIVE_PATH = r"G:\Il mio Drive\Fatturazione"
CONFIG_FILE = os.path.join(DRIVE_PATH, "MESE_IN_CORSO.txt")

# IL NOSTRO NUOVO PONTE DI COLLEGAMENTO WEB
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbytrRhUjnITTDO7Y6OxeDSKomuVR3ezsEoRKNClFS2m1poYul-yHYG64XEy_BjVM8Y83w/exec"

def get_mese_in_corso():
    if not os.path.exists(CONFIG_FILE):
        print("❌ ERRORE: MESE_IN_CORSO.txt non trovato. Esegui prima 1_Riepiloghi_Giornalieri.py!")
        sys.exit(1)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

# Mappatura dai nomi dei viaggi dal file KM alle intestazioni Foglio Master
mapping_nomi = {
    "VR": "VR",
    "VR MN": "VR - MN",
    "LAGO 1": "LAGO BS 1",
    "LAGO 2": "LAGO BS 2",
    "BS 1": "LAGO BS 1",  
    "BS 2": "LAGO BS 2",
    "EXTRA": "EXTRA",
    "BL 1": "LS BL1",
    "BL 2": "LS BL2",
    "BL 3": "LS BL3",
    "BL 4": "LS BL4",
    "BL 5": "LS BL5"
}

def is_fixed_route(target_excel):
    fissi = ["VR", "VR - MN", "LAGO BS 1", "LAGO BS 2"]
    return target_excel in fissi

def aggiorna_fatturazione():
    mese = get_mese_in_corso()
    RIEPILOGO_FILE = os.path.join(DRIVE_PATH, "Riepiloghi_Giornalieri", mese, f"Riepilogo_KM_Mensile_{mese.upper()}.xlsx")
    
    # Taglia "marzo 2026" in "MARZO"
    FOGLIO_MESE = "".join([c for c in mese.upper() if c.isalpha()])
    
    if not os.path.exists(RIEPILOGO_FILE):
        print(f"❌ File locale {RIEPILOGO_FILE} non trovato. Lancia lo script 2!")
        return
        
    print(f"🔍 Lettura chilometri calcolati da local: {RIEPILOGO_FILE}")
    print(f"🎯 Preparazione sincronizzazione CLOUD verso linguetta nativa: [{FOGLIO_MESE}]")
    
    df_km = pd.read_excel(RIEPILOGO_FILE)
    df_km['Data'] = pd.to_datetime(df_km['Data']).dt.date
    
    modifiche = 0
    errori = 0
    
    print("\n🚀 Inizio decollo dati verso Google Sheets...\n")
    
    for idx, row in df_km.iterrows():
        giorno = row['Data']
        # Estraiamo il numerino (es. 27). Questo servirà all'App Web per trovare la colonna!
        giorno_numerico = giorno.day
        
        for col_name in row.index:
            if col_name == 'Data' or pd.isna(row[col_name]) or row[col_name] == 0:
                continue 
                
            km_calcolati = row[col_name]
            
            if col_name in mapping_nomi:
                target_excel = mapping_nomi[col_name]
                
                # Valore standardizzato: i fissi hanno quota 350
                if is_fixed_route(target_excel):
                    valore_da_scrivere = 350
                else:
                    valore_da_scrivere = int(km_calcolati)
                
                # Definizione delle Note (solo su NON Belluno) e Tappe
                num_tappe = None
                testo_nota = ""
                
                if not target_excel.startswith("LS BL"):
                    col_tappe = f"{col_name}_tappe"
                    num_tappe = int(row[col_tappe]) if col_tappe in row.index and not pd.isna(row[col_tappe]) else None
                    if num_tappe is not None:
                        testo_nota = f"KM Reali Google: {int(km_calcolati)}\nTappe: {num_tappe}"
                    else:
                        testo_nota = f"KM Reali Google: {int(km_calcolati)}"
                    
                # Regola cromatica gialla per > 15 fermate (HEX standard senza cancelletto)
                colore_cella = None
                if num_tappe is not None and num_tappe > 15:
                    colore_cella = "FFFF00"
                    
                # Impacchettiamo tutte le istruzioni da inviare al server Google
                payload = {
                    "sheet_name": FOGLIO_MESE,
                    "day": giorno_numerico,
                    "route_target": target_excel,
                    "km_value": valore_da_scrivere,
                    "comment": testo_nota,
                    "color": colore_cella
                }
                
                # Invio fulmineo della richiesta HTTP POST
                try:
                    r = requests.post(WEBHOOK_URL, json=payload)
                    try:
                        res = r.json()
                        if res.get("status") == "ok":
                            modifiche += 1
                            print(f"📡 CONSEGNATO IN CLOUD -> Giorno {giorno_numerico} | {target_excel}: {valore_da_scrivere} km")
                        else:
                            errori += 1
                            print(f"⚠️ ERRORE GOOGLE SHEET: {res.get('message')} per {target_excel} (Giorno {giorno_numerico})")
                    except Exception as json_err:
                        errori += 1
                        print(f"⚠️ RISPOSTA ANOMALA GOOGLE. HTTP: {r.status_code}. \nTesto Ricevuto: {r.text[:300]}")
                        
                except Exception as e:
                    errori += 1
                    print(f"🔌 Errore di rete: {e}")

    print("\n==================================")
    print(f"✅ Sincronizzazione WEB 100% Completata.")
    print(f"Cellule aggiornate online: {modifiche}")
    if errori > 0:
        print(f"Errori registrati (Es. foglio/riga inesistente): {errori}")
    print("==================================")

if __name__ == "__main__":
    aggiorna_fatturazione()
