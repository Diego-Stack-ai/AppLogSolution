import os
import pandas as pd
import json
from datetime import datetime

# Cartella corrente dove si trovano i file .xlsx
cartella = os.path.dirname(os.path.abspath(__file__))

tutti_i_dati = []

# Scansiona tutti i file nella cartella
for file in os.listdir(cartella):
    if file.endswith(".xlsx") and not file.startswith("~$"):
        percorso = os.path.join(cartella, file)
        autista = file.replace(".xlsx", "").strip()
        print(f"Elaborazione file: {autista}...")
        
        try:
            # Leggi tutti i fogli (linguette dei mesi)
            excel_file = pd.ExcelFile(percorso)
            
            for mese in excel_file.sheet_names:
                df = pd.read_excel(percorso, sheet_name=mese)
                
                # Rinomina colonne per sicurezza o usa gli indici (0=Data, 1=Cliente, ecc.)
                # In pandas le colonne possono avere spazi strani, quindi iteriamo sulle righe
                for index, row in df.iterrows():
                    data_cella = row.iloc[0]
                    
                    # Salta se la data è nulla o non è un datetime
                    if pd.isna(data_cella) or not isinstance(data_cella, datetime):
                        continue
                        
                    try:
                        # Estrazione campi in base alla posizione della colonna
                        # 0:'Data', 1:'Cliente', 4:'Delta Km', 5:'Ora inizio m', 6:'Ora fine m', 9:'Orario giornaliero', 12:'NOTE...'
                        ore_totali = row.iloc[9] if not pd.isna(row.iloc[9]) else 0
                        km_delta = row.iloc[4] if not pd.isna(row.iloc[4]) else 0
                        cliente = str(row.iloc[1]) if not pd.isna(row.iloc[1]) else ""
                        ora_in = str(row.iloc[5]) if not pd.isna(row.iloc[5]) else ""
                        ora_out = str(row.iloc[6]) if not pd.isna(row.iloc[6]) else ""
                        note = str(row.iloc[12]) if len(row) > 12 and not pd.isna(row.iloc[12]) else ""
                        
                        # Fix per orari (se sono oggetti time)
                        if hasattr(row.iloc[5], 'strftime'): ora_in = row.iloc[5].strftime('%H:%M')
                        if hasattr(row.iloc[6], 'strftime'): ora_out = row.iloc[6].strftime('%H:%M')
                        
                        tutti_i_dati.append({
                            "autista": autista,
                            "mese": mese,
                            "data": data_cella.strftime("%Y-%m-%dT00:00:00.000Z"), # Formato ISO compatibile col JS
                            "cliente": cliente,
                            "kmDelta": float(km_delta) if str(km_delta).replace('.','',1).isdigit() else 0,
                            "oraInizioM": ora_in,
                            "oraFineM": ora_out,
                            "oreTotali": float(ore_totali) if str(ore_totali).replace('.','',1).isdigit() else 0,
                            "note": note
                        })
                    except Exception as e:
                        print(f"  [!] Errore riga {index} del mese {mese}: {e}")
                        
        except Exception as e:
            print(f"Errore caricamento file {file}: {e}")

# Ordina per data crescente
tutti_i_dati.sort(key=lambda x: x["data"])

# Salva in formato JSON
file_output = os.path.join(cartella, "dati_presenze.json")
with open(file_output, "w", encoding="utf-8") as f:
    json.dump(tutti_i_dati, f, ensure_ascii=False, indent=2)

print(f"\nOperazione completata! Creato file: {file_output}")
print(f"Totale record estratti: {len(tutti_i_dati)}")
