import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import sys

# 1. Connessione a Firebase
cred = credentials.Certificate('prod_key.json')
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    pass

db = firestore.client()

print("Recupero clienti CATTEL da Firestore...")
clienti_ref = db.collection('clienti').document('CATTEL').collection('raccolta clienti')
docs = list(clienti_ref.stream())

clienti_db = []
for doc in docs:
    d = doc.to_dict()
    clienti_db.append({
        'id': doc.id,
        'nome': (d.get('cliente') or d.get('nome_consegna') or '').strip(),
        'indirizzo': (d.get('indirizzo') or d.get('ind') or '').strip(),
        'codice_frutta': d.get('codice_frutta', ''),
        'codice_latte': d.get('codice_latte', '')
    })

print(f"Trovati {len(clienti_db)} clienti nel DB.")

# 2. Lettura Excel
excel_path = 'ReportPianificazione.xlsx'
try:
    xl = pd.ExcelFile(excel_path)
except Exception as e:
    print(f"Errore caricamento Excel: {e}")
    sys.exit(1)

print(f"Fogli trovati: {xl.sheet_names}")

clienti_excel = []
for sheet_name in xl.sheet_names:
    if sheet_name.lower() == 'riepilogo':
        continue
    
    df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)
    
    autista = str(df.iloc[1, 2]).strip() if len(df) > 1 and len(df.columns) > 2 else ""
    
    # Header is at row 4 (index 3)
    # Magazzino partenza at row 5 (index 4)
    # Magazzino arrivo is the last row
    
    if len(df) <= 5:
        continue
        
    last_idx = len(df) - 1
    
    for i in range(5, last_idx):
        row = df.iloc[i]
        codice = str(row.iloc[0]).strip()
        nome = str(row.iloc[1]).strip()
        indirizzo = str(row.iloc[2]).strip()
        colli = str(row.iloc[9]).strip() if len(row) > 9 else ""
        
        if not codice or codice.lower() == 'nan':
            continue
            
        clienti_excel.append({
            'foglio': sheet_name,
            'codice': codice,
            'nome': nome,
            'indirizzo': indirizzo
        })

print(f"Trovati {len(clienti_excel)} clienti nel file Excel (esclusi magazzini e riepilogo).")

# 3. Tentativo di abbinamento per nome
matched = 0
for db_cli in clienti_db:
    nome_db_lower = db_cli['nome'].lower()
    
    best_match = None
    for ex_cli in clienti_excel:
        if nome_db_lower in ex_cli['nome'].lower() or ex_cli['nome'].lower() in nome_db_lower:
            best_match = ex_cli
            break
            
    if best_match:
        matched += 1
        print(f"MATCH TROVATO: DB[{db_cli['nome']}] -> Excel[{best_match['nome']} | Codice: {best_match['codice']}]")

print(f"Totale match trovati: {matched}/{len(clienti_db)}")
