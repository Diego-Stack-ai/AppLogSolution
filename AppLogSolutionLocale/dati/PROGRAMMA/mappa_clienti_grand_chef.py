import os
import sys
import re
import shutil
import requests
import pandas as pd
from pathlib import Path

# Configurazione Percorsi
BASE_DIR = Path(__file__).resolve().parent.parent
BELLUNO_DIR = BASE_DIR / "Belluno"
MASTER_DB_PATH = BASE_DIR / "PROGRAMMA" / "mappatura_destinazioni.xlsx"
WEB_DB_PATH = Path("g:/Il mio Drive/App/AppLogSolutionsWeb/Progetto Scuole/PROGRAMMA/mappatura_destinazioni.xlsx")

# API Key Google Maps
GOOGLE_MAPS_API_KEY = "AIzaSyAHQ3HjuEEIS8bn5KMh6N3UoM6kZ2MYGL4"

def geocode_address(address, city, prov):
    """
    Effettua la geocodifica dell'indirizzo tramite l'API di Google Maps.
    Ritorna: (lat, lng, cap, status)
    """
    full_address = f"{address}, {city} ({prov}), Italia"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={requests.utils.quote(full_address)}&key={GOOGLE_MAPS_API_KEY}"
    try:
        resp = requests.get(url, timeout=10).json()
        if resp.get("status") == "OK":
            location = resp["results"][0]["geometry"]["location"]
            # Estrae anche il CAP se presente
            cap = ""
            for component in resp["results"][0]["address_components"]:
                if "postal_code" in component["types"]:
                    cap = component["long_name"]
            return location["lat"], location["lng"], cap, "OK"
    except Exception as e:
        print(f"Errore durante la chiamata di geocodifica: {e}")
    return None, None, "", "ERROR"

def clean_client_code(code_val):
    """
    Ripulisce il codice cliente rimuovendo eventuali spazi ed estensioni decimali (es: '123.0' -> '123').
    """
    if pd.isna(code_val):
        return ""
    code_str = str(code_val).strip()
    if code_str.endswith(".0"):
        code_str = code_str[:-2]
    return code_str

def parse_fascia_oraria(val):
    """
    Parsifica la stringa Fascia oraria o Note e ritorna (orario_min, orario_max).
    Esempi:
      '07:00  11:30' -> ('07:00', '11:30')
      'Dopo le 08:30' -> ('08:30', '')
      'Entro le 11:30' -> ('', '11:30')
    """
    if pd.isna(val):
        return "", ""
    
    val_str = str(val).strip()
    
    # 1. Cerca due orari HH:MM (range standard)
    match_range = re.findall(r'(\d{2}:\d{2})', val_str)
    if len(match_range) == 2:
        return match_range[0], match_range[1]
    
    # 2. Cerca 'Dopo le HH:MM'
    match_dopo = re.search(r'(?:Dopo le|dopo le)\s*(\d{2}:\d{2})', val_str)
    if match_dopo:
        return match_dopo.group(1), ""
        
    # 3. Cerca 'Entro le HH:MM'
    match_entro = re.search(r'(?:Entro le|entro le)\s*(\d{2}:\d{2})', val_str)
    if match_entro:
        return "", match_entro.group(1)
        
    return "", ""

def main():
    print("="*60)
    print(">>> SCRIPT IMPORTAZIONE AVANZATA CLIENTI GRAND CHEF (CON ORARI & NOTE) <<<")
    print("="*60)
    
    # 1. Verifica esistenza file e cartelle
    if not BELLUNO_DIR.exists():
        print(f"Errore: Cartella dei file Belluno non trovata in: {BELLUNO_DIR}")
        sys.exit(1)
        
    if not MASTER_DB_PATH.exists():
        print(f"Errore: Database master mappatura_destinazioni.xlsx non trovato in: {MASTER_DB_PATH}")
        sys.exit(1)
        
    # Carica database master esistente
    print(f"Caricamento master Excel: {MASTER_DB_PATH}")
    try:
        df_master = pd.read_excel(MASTER_DB_PATH)
        # Forza i codici in formato stringa ripulita per evitare disallineamenti di tipo
        df_master['Codice Frutta'] = df_master['Codice Frutta'].apply(clean_client_code)
    except Exception as e:
        print(f"Errore nel caricamento del database master: {e}")
        sys.exit(1)
        
    print(f"Master Excel caricato. Record esistenti: {len(df_master)}")
    
    # Assicura che la colonna 'Note' esista nel master
    if 'Note' not in df_master.columns:
        print("Creazione della colonna 'Note' nel master Excel...")
        df_master['Note'] = ""
    
    # 2. Scansione dei file Excel in dati/Belluno/ ordinati per data di modifica disk
    files = list(BELLUNO_DIR.glob("*.xlsx"))
    if not files:
        print(f"Nessun file Excel trovato in {BELLUNO_DIR}")
        sys.exit(0)
        
    print(f"Trovati {len(files)} file Excel nella cartella Belluno.")
    
    # Dizionario per memorizzare i dati dei clienti unici.
    # Struttura: { codice_cliente: { dati_del_cliente, mtime_del_file_origine } }
    clienti_mappati = {}
    
    for f in files:
        try:
            mtime = f.stat().st_mtime
            df = pd.read_excel(f, sheet_name=0)
            df_clean = df.dropna(how='all')
            
            # Individua la riga dell'intestazione (cerca colonne 'Ragione Sociale' o 'Codice ')
            header_row_idx = None
            for idx, row in df_clean.iterrows():
                row_vals = [str(val).strip().lower() for val in row.values if pd.notna(val)]
                if any('ragione sociale' in rv for rv in row_vals) or any('codice' in rv for rv in row_vals):
                    header_row_idx = idx
                    break
                    
            if header_row_idx is None:
                continue
                
            # Righe di dati effettivi (sotto l'intestazione)
            df_data = df_clean.loc[header_row_idx + 1:]
            
            for _, row in df_data.iterrows():
                # Salta la riga finale del 'Totale'
                if str(row.iloc[0]).lower().strip() == 'totale':
                    continue
                    
                codice = clean_client_code(row.iloc[0])
                ragione_sociale = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
                indirizzo = str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else ""
                localita = str(row.iloc[7]).strip() if pd.notna(row.iloc[7]) else ""
                provincia = str(row.iloc[8]).strip() if pd.notna(row.iloc[8]) else ""
                
                # Legge Note (Col 14) e Fascia oraria (Col 15)
                note = str(row.iloc[14]).strip() if len(row) > 14 and pd.notna(row.iloc[14]) else ""
                fascia = str(row.iloc[15]).strip() if len(row) > 15 and pd.notna(row.iloc[15]) else ""
                
                if not codice or not ragione_sociale or ragione_sociale == "nan":
                    continue
                    
                # Estrae e pulisce gli orari
                orario_min, orario_max = parse_fascia_oraria(fascia)
                if not orario_min and not orario_max and note:
                    # Fallback intelligente: se la fascia oraria è vuota, prova a leggerla dalle Note
                    orario_min, orario_max = parse_fascia_oraria(note)
                
                client_dati = {
                    "codice": codice,
                    "ragione_sociale": ragione_sociale,
                    "indirizzo": indirizzo,
                    "localita": localita,
                    "provincia": provincia,
                    "note": note,
                    "orario_min": orario_min,
                    "orario_max": orario_max,
                    "file_origine": f.name,
                    "file_mtime": mtime
                }
                
                # [REQUISITO CONFLITTI]: In caso di duplicato, tieni il dato del file più recente
                if codice in clienti_mappati:
                    stored_mtime = clienti_mappati[codice]["file_mtime"]
                    if mtime > stored_mtime:
                        # Il file attuale è più nuovo, sovrascrivi
                        clienti_mappati[codice] = client_dati
                else:
                    clienti_mappati[codice] = client_dati
                    
        except Exception as e:
            print(f"Errore nell'elaborazione del file {f.name}: {e}")
            
    print(f"Estrazione completata. Clienti Grand Chef unici da importare: {len(clienti_mappati)}")
    
    # 3. Importazione incrementale con gestione corretta degli stati 'ok'
    skipped_count = 0
    updated_only_logistics_count = 0
    updated_all_count = 0
    inserted_count = 0
    
    for codice, c in clienti_mappati.items():
        rs = c['ragione_sociale']
        ind = c['indirizzo']
        loc = c['localita']
        pr = c['provincia']
        note = c['note']
        o_min = c['orario_min']
        o_max = c['orario_max']
        
        # Cerca se il codice esiste già in 'Codice Frutta' del master
        mask = df_master['Codice Frutta'] == codice
        
        if mask.any():
            # Il cliente esiste già
            idx = df_master[mask].index[0]
            stato_corrente = str(df_master.at[idx, 'Stato geocoding']).strip().lower()
            
            if stato_corrente == 'ok':
                # [REQUISITO CONFLITTO 'OK']: Non sovrascrivere coordinate e stato,
                # ma AGGIORNA comunque orari e note dal file più recente!
                print(f"[AGGIORNA LOGISTICA] Cliente {codice:10} | {rs[:35]:35} | Già OK. Aggiornati orari ({o_min}-{o_max}) e note.")
                df_master.at[idx, 'Orario min Frutta'] = o_min
                df_master.at[idx, 'Orario max Frutta'] = o_max
                df_master.at[idx, 'Orario min Latte'] = o_min
                df_master.at[idx, 'Orario max Latte'] = o_max
                df_master.at[idx, 'Note'] = note
                updated_only_logistics_count += 1
            else:
                # Il cliente esiste ma non è ancora confermato 'ok'. Aggiorna tutto, coordinate incluse.
                print(f"[AGGIORNA COMPLETO]  Cliente {codice:10} | {rs[:35]:35} | Rigeocodifica in corso...")
                lat, lon, cap, status = geocode_address(ind, loc, pr)
                
                df_master.at[idx, 'A chi va consegnato'] = rs
                df_master.at[idx, 'Indirizzo'] = ind
                df_master.at[idx, 'Città'] = loc
                df_master.at[idx, 'Provincia'] = pr
                df_master.at[idx, 'Tipologia grado'] = "GRAND CHEF"
                df_master.at[idx, 'Codice Latte'] = "p00000"
                df_master.at[idx, 'Orario min Frutta'] = o_min
                df_master.at[idx, 'Orario max Frutta'] = o_max
                df_master.at[idx, 'Orario min Latte'] = o_min
                df_master.at[idx, 'Orario max Latte'] = o_max
                df_master.at[idx, 'Note'] = note
                
                if status == "OK":
                    df_master.at[idx, 'Latitudine'] = lat
                    df_master.at[idx, 'Longitudine'] = lon
                    df_master.at[idx, 'CAP'] = cap
                    df_master.at[idx, 'Stato geocoding'] = ""  # Stato vuoto = verde (non ancora confermato)
                else:
                    df_master.at[idx, 'Latitudine'] = 0
                    df_master.at[idx, 'Longitudine'] = 0
                    df_master.at[idx, 'Stato geocoding'] = "not_found"  # Stato rosso (mancante)
                updated_all_count += 1
        else:
            # Il cliente non esiste, lo inseriamo come nuovo record completo
            print(f"[INSERISCI NUOVO]    Cliente {codice:10} | {rs[:35]:35} | Nuova geocodifica in corso...")
            lat, lon, cap, status = geocode_address(ind, loc, pr)
            
            new_row = {
                "Codice Frutta": codice,
                "Codice Latte": "p00000",
                "A chi va consegnato": rs,
                "Tipologia grado": "GRAND CHEF",
                "Indirizzo": ind,
                "CAP": cap if status == "OK" else "",
                "Città": loc,
                "Provincia": pr,
                "Orario min Frutta": o_min,
                "Orario max Frutta": o_max,
                "Orario min Latte": o_min,
                "Orario max Latte": o_max,
                "Note": note,
                "Latitudine": lat if status == "OK" else 0,
                "Longitudine": lon if status == "OK" else 0,
                "Stato geocoding": "" if status == "OK" else "not_found"  # Vuoto per verde, "not_found" per rosso
            }
            
            # Aggiunge le colonne vuote per mantenere la struttura intatta
            for col in df_master.columns:
                if col not in new_row:
                    new_row[col] = None
                    
            df_master = pd.concat([df_master, pd.DataFrame([new_row])], ignore_index=True)
            inserted_count += 1

    # 4. Salvataggio del Master Excel locale
    print(f"\nSalvataggio del master Excel locale in: {MASTER_DB_PATH}")
    try:
        # Pulisce colonne fittizie introdotte temporaneamente se non necessarie (ad es. file_origine o simili)
        df_master = df_master.loc[:, ~df_master.columns.str.contains('^Unnamed:')]
        df_master.to_excel(MASTER_DB_PATH, index=False)
        print("Salvataggio locale completato con successo!")
    except Exception as e:
        print(f"Errore durante il salvataggio del master locale: {e}")
        sys.exit(1)
        
    # 5. Sincronizzazione con il database master Web
    print(f"Allineamento con la parità web in: {WEB_DB_PATH}")
    try:
        WEB_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(MASTER_DB_PATH, WEB_DB_PATH)
        print("Allineamento con la parità web completato con successo!")
    except Exception as e:
        print(f"Avviso: impossibile allineare direttamente con il repository web: {e}")

    # Statistiche finali
    print("\n" + "="*40)
    print(">>> STATISTICHE DI IMPORTAZIONE GLOBALE <<<")
    print(f"Nuovi record inseriti: {inserted_count}")
    print(f"Record esistenti aggiornati COMPLETAMENTE (non OK): {updated_all_count}")
    print(f"Record OK aggiornati SOLO per orari/note: {updated_only_logistics_count}")
    print(f"Numero totale righe master finale: {len(df_master)}")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()
