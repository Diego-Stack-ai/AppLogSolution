import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import sys
import os

# 1. Inizializzazione Firebase
cred = credentials.Certificate('dev_key.json')
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    pass

db = firestore.client()

# Cancellazione vecchie anomalie Cattel pendenti (opzionale/pulizia)
print("Pulizia anomalie pendenti CATTEL (se presenti)...")
jobs_ref = db.collection('clienti').document('CATTEL').collection('processing_jobs')
docs = list(jobs_ref.where('status', 'in', ['da_mappare', 'pending']).stream())
for doc in docs:
    doc.reference.delete()
    print(f"Cancellato job anomalo {doc.id}")

# 2. Lettura Clienti CATTEL salvati nel DB
print("Recupero clienti CATTEL da Firestore...")
clienti_ref = db.collection('clienti').document('CATTEL').collection('raccolta clienti')
db_docs = list(clienti_ref.stream())

clienti_db = []
for doc in db_docs:
    d = doc.to_dict()
    clienti_db.append({
        'id': doc.id,
        'doc_ref': doc.reference,
        'nome': (d.get('cliente') or d.get('nome_consegna') or '').strip()
    })

print(f"Trovati {len(clienti_db)} clienti geolocalizzati nel DB.")

# 3. Lettura multipla dei file Excel
files_to_read = [
    'ReportPianificazione.xlsx',
    'ReportPianificazione (3).xlsx',
    'ReportPianificazione (4).xlsx',
    'ReportPianificazione (5).xlsx'
]

clienti_excel = {}

for excel_path in files_to_read:
    if not os.path.exists(excel_path):
        print(f"File non trovato: {excel_path}")
        continue
        
    try:
        xl = pd.ExcelFile(excel_path)
    except Exception as e:
        print(f"Errore caricamento {excel_path}: {e}")
        continue

    for sheet_name in xl.sheet_names:
        if sheet_name.lower() == 'riepilogo':
            continue
        
        df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)
        
        if len(df) <= 5:
            continue
            
        last_idx = len(df) - 1
        
        for i in range(5, last_idx):
            row = df.iloc[i]
            codice = str(row.iloc[0]).strip()
            nome = str(row.iloc[1]).strip()
            
            if not codice or codice.lower() == 'nan':
                continue
                
            # Usiamo il nome normalizzato come chiave per deduplicare
            norm_name = nome.lower().strip()
            if norm_name not in clienti_excel:
                clienti_excel[norm_name] = {
                    'nome_originale': nome,
                    'codice': codice,
                    'file_origine': excel_path
                }

print(f"Estratti {len(clienti_excel)} clienti univoci dai file Excel.")

# 4. Abbinamento Esatto e Aggiornamento
matched_count = 0
unmatched_list = []

for db_cli in clienti_db:
    nome_db_norm = db_cli['nome'].lower().strip()
    
    # Check "Exact Match"
    if nome_db_norm in clienti_excel:
        match = clienti_excel[nome_db_norm]
        
        # AGGIORNAMENTO SU FIRESTORE
        db_cli['doc_ref'].update({
            'codice_frutta': match['codice'],
            'codice_latte': 'P00000'
        })
        
        print(f"AGGIORNATO: {db_cli['nome']} -> Codice: {match['codice']}")
        matched_count += 1
    else:
        unmatched_list.append(db_cli['nome'])

print(f"\nOperazione conclusa. Aggiornati {matched_count}/{len(clienti_db)} clienti.")

# 5. Generazione Report per i non abbinati
with open('report_clienti_non_abbinati.md', 'w', encoding='utf-8') as f:
    f.write("# Report Clienti Non Abbinati\n\n")
    f.write("I seguenti clienti presenti nel Database CATTEL non hanno trovato un riscontro ESATTO nei file Excel forniti.\n\n")
    
    if len(unmatched_list) == 0:
        f.write("**Tutti i clienti sono stati abbinati con successo!**\n")
    else:
        for name in unmatched_list:
            f.write(f"- {name}\n")

print(f"Report generato in 'report_clienti_non_abbinati.md'. Clienti non trovati: {len(unmatched_list)}")
