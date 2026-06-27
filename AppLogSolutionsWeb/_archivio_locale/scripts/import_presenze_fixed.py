import os
import re
from datetime import datetime
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

SERVICE_ACCOUNT_PATH = r"g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json"
CARTELLA_AGGIORNAMENTi = r"g:\Il mio Drive\App\AppLogSolutionsWeb\Presenze\Presenze aggiornate"

if not os.path.exists(SERVICE_ACCOUNT_PATH):
    print(f"Errore: File service account non trovato in {SERVICE_ACCOUNT_PATH}")
    exit(1)

try:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
except ValueError:
    pass

db = firestore.client()

def normalizza_nome(nome):
    nome = re.sub(r"[A-Z]{2}\d{3}[A-Z]{2}", "", nome, flags=re.IGNORECASE)
    nome = nome.replace(".xlsx", "")
    nome = nome.lower().replace("k", "c").replace("_", " ")
    return " ".join(nome.split())

def match_autista(nome_file, lista_autisti):
    nome_norm = normalizza_nome(nome_file)
    for autista in lista_autisti:
        if normalizza_nome(autista["nome"]) == nome_norm:
            return autista["id"], autista["nome"]
            
    for autista in lista_autisti:
        nome_fb_norm = normalizza_nome(autista["nome"])
        parole_fb = nome_fb_norm.split()
        if all(p in nome_norm for p in parole_fb):
            return autista["id"], autista["nome"]
            
    parole_file = nome_norm.split()
    for autista in lista_autisti:
        nome_fb_norm = normalizza_nome(autista["nome"])
        if all(p in nome_fb_norm for p in parole_file):
            return autista["id"], autista["nome"]
            
    parole_lunghe = [p for p in parole_file if len(p) > 4]
    for autista in lista_autisti:
        nome_fb_norm = normalizza_nome(autista["nome"])
        for p in parole_lunghe:
            if p in nome_fb_norm:
                return autista["id"], autista["nome"]

    return None, None

def find_column_index(columns, possible_names):
    for i, col in enumerate(columns):
        col_str = str(col).lower().strip()
        for name in possible_names:
            if col_str == name.lower() or col_str.startswith(name.lower()):
                return i
    return -1

def fix_time(val):
    if not val or val == "-": return ""
    val = str(val).strip()
    if val.endswith(".5"):
        parts = val.split(".")
        return f"{int(parts[0]):02d}:30"
    if val.endswith(".0"):
        parts = val.split(".")
        return f"{int(parts[0]):02d}:00"
    if val.isdigit():
        return f"{int(val):02d}:00"
    if ":" in val:
        parts = val.split(":")
        if len(parts) == 2 and parts[0].isdigit():
            return f"{int(parts[0]):02d}:{parts[1]}"
    return val

def format_time(t):
    if pd.isna(t):
        return ""
    if hasattr(t, "strftime"):
        return t.strftime("%H:%M")
    return fix_time(str(t).strip())

def is_valid_time(t):
    if not t: return True
    return bool(re.match(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$", t))

def processa_aggiornamenti():
    print(f"--- INIZIO IMPORTAZIONE DINAMICA DA {CARTELLA_AGGIORNAMENTi} ---")
    files = [f for f in os.listdir(CARTELLA_AGGIORNAMENTi) if f.endswith(".xlsx") and not f.startswith("~$")]

    autisti_ref = db.collection("dipendenti").stream()
    lista_autisti = []
    for doc in autisti_ref:
        data = doc.to_dict()
        lista_autisti.append({
            "id": doc.id,
            "nome": data.get("nome", "")
        })

    batch = db.batch()
    operazioni_batch = 0
    totale_record = 0

    for file in files:
        percorso = os.path.join(CARTELLA_AGGIORNAMENTi, file)
        nome_base = file.replace(".xlsx", "").strip()
        print(f"\nElaborazione file: {nome_base}")
        
        autista_id, autista_nome = match_autista(nome_base, lista_autisti)
        if not autista_id:
            print(f"  [ATTENZIONE] Impossibile trovare un match in Firebase per: {nome_base}")
            continue
            
        print(f"  --> Match trovato: {autista_nome}")
        
        try:
            excel_file = pd.ExcelFile(percorso)
            for sheet in excel_file.sheet_names:
                df = pd.read_excel(percorso, sheet_name=sheet)
                cols = df.columns.tolist()
                
                idx_data = find_column_index(cols, ["data"])
                if idx_data == -1:
                    print(f"  [!] Colonna Data non trovata nel foglio {sheet}")
                    continue
                    
                idx_cliente = find_column_index(cols, ["cliente", "destinazione"])
                idx_km = find_column_index(cols, ["delta km", "km delta"])
                idx_orain_m = find_column_index(cols, ["ora inizio"])
                idx_oraout_m = find_column_index(cols, ["ora fine"])
                idx_orain_p = find_column_index(cols, ["ora inizio.1"])
                idx_oraout_p = find_column_index(cols, ["ora fine.1"])
                idx_ore = find_column_index(cols, ["orario giornaliero", "orario ordinarie", "totale ore", "ore totali"])
                idx_extra = find_column_index(cols, ["ore straordinarie"])
                idx_note = find_column_index(cols, ["note"])
                
                is_2_columns = (idx_orain_p == -1 and idx_oraout_p == -1)
                
                for index, row in df.iterrows():
                    data_cella = row.iloc[idx_data]
                    if pd.isna(data_cella) or not isinstance(data_cella, datetime):
                        continue
                        
                    cliente = str(row.iloc[idx_cliente]) if idx_cliente != -1 and not pd.isna(row.iloc[idx_cliente]) else ""
                    km_delta = row.iloc[idx_km] if idx_km != -1 and not pd.isna(row.iloc[idx_km]) else 0
                    
                    ora_in_m_raw = format_time(row.iloc[idx_orain_m]) if idx_orain_m != -1 else ""
                    ora_out_m_raw = format_time(row.iloc[idx_oraout_m]) if idx_oraout_m != -1 else ""
                    ora_in_p_raw = format_time(row.iloc[idx_orain_p]) if idx_orain_p != -1 else ""
                    ora_out_p_raw = format_time(row.iloc[idx_oraout_p]) if idx_oraout_p != -1 else ""
                    
                    if is_2_columns:
                        ora_in_m = ora_in_m_raw
                        ora_out_p = ora_out_m_raw
                        ora_out_m = ""
                        ora_in_p = ""
                    else:
                        ora_in_m = ora_in_m_raw
                        ora_out_m = ora_out_m_raw
                        ora_in_p = ora_in_p_raw
                        ora_out_p = ora_out_p_raw
                        
                    has_error = not (is_valid_time(ora_in_m) and is_valid_time(ora_out_m) and is_valid_time(ora_in_p) and is_valid_time(ora_out_p))
                    
                    ore_tot = row.iloc[idx_ore] if idx_ore != -1 and not pd.isna(row.iloc[idx_ore]) else 0
                    ore_straord = row.iloc[idx_extra] if idx_extra != -1 and not pd.isna(row.iloc[idx_extra]) else 0
                    note = str(row.iloc[idx_note]) if idx_note != -1 and not pd.isna(row.iloc[idx_note]) else ""
                    
                    data_iso = data_cella.strftime("%Y-%m-%dT00:00:00.000Z")
                    mese_str = data_cella.strftime("%Y-%m")
                    doc_id = f"{autista_id}_{data_cella.strftime('%Y-%m-%d')}"
                    
                    doc_ref = db.collection("presenze").document(doc_id)
                    data_obj = {
                        "autistaId": autista_id,
                        "autista": autista_nome,
                        "mese": mese_str,
                        "data": data_iso,
                        "cliente": cliente,
                        "kmDelta": float(km_delta) if str(km_delta).replace(".","",1).isdigit() else 0,
                        "oraInizioM": ora_in_m,
                        "oraFineM": ora_out_m,
                        "oraInizioP": ora_in_p,
                        "oraFineP": ora_out_p,
                        "oreTotali": (float(ore_tot) if str(ore_tot).replace(".", "", 1).isdigit() else 0) + (float(ore_straord) if str(ore_straord).replace(".", "", 1).isdigit() else 0),
                        "oreOrdinarie": float(ore_tot) if str(ore_tot).replace(".","",1).isdigit() else 0,
                        "oreStraordinarie": float(ore_straord) if str(ore_straord).replace(".","",1).isdigit() else 0,
                        "note": note,
                        "hasError": has_error
                    }
                    batch.set(doc_ref, data_obj, merge=True)
                    
                    operazioni_batch += 1
                    totale_record += 1
                    
                    if operazioni_batch >= 400:
                        batch.commit()
                        batch = db.batch()
                        operazioni_batch = 0

        except Exception as e:
            print(f"  [!] Errore: {e}")

    if operazioni_batch > 0:
        batch.commit()
        
    print(f"\n--- COMPLETATO! {totale_record} record salvati ---")

if __name__ == "__main__":
    processa_aggiornamenti()

