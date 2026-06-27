import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import math

cred = credentials.Certificate('G:/Il mio Drive/App/AppLogSolutions/backend/config/log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def s(val):
    if pd.isna(val): return ""
    if isinstance(val, (int, float)) and math.isnan(val): return ""
    return str(val).strip()

print("1. Aggiornamento 'mappatura' in Firestore...")
df_map = pd.read_excel('G:/Il mio Drive/App/AppLogSolutions/dati/PROGRAMMA/mappatura_destinazioni.xlsx', dtype=str)
batch = db.batch()
count = 0
for idx, row in df_map.iterrows():
    c_f = s(row.get('Codice Frutta'))
    c_l = s(row.get('Codice Latte'))
    if c_f == "p00000" and c_l == "p00000": continue
    if not c_f and not c_l: continue
    
    doc_id = c_f if (c_f and c_f != "p00000") else c_l
    doc_ref = db.collection('mappatura').document(str(doc_id).replace("/", "_").replace(".", "_"))
    
    data = {
        "codice_frutta": c_f,
        "codice_latte": c_l,
        "cliente": s(row.get('Mensa / Sede')) or s(row.get('A chi va consegnato')),
        "nome_consegna": s(row.get('A chi va consegnato')),
        "indirizzo": s(row.get('Indirizzo')),
        "cap": s(row.get('CAP')),
        "citta": s(row.get("Località")) or s(row.get("Localit\u00E0")) or s(row.get("Citta")) or s(row.get("Citt\u00E0")),
        "prov": s(row.get('Pr.')),
        "lat": s(row.get('Latitudine')),
        "lon": s(row.get('Longitudine'))
    }
    batch.set(doc_ref, data, merge=True)
    count += 1
    if count % 400 == 0:
        batch.commit()
        batch = db.batch()

batch.commit()
print(f"-> Mappatura caricata! ({count} record)\n")

print("2. Aggiornamento 'articoli' in Firestore...")
df_art = pd.read_excel('G:/Il mio Drive/App/AppLogSolutions/dati/tabella_aggiornamento_articoli.xlsx', dtype=str)
batch = db.batch()
count = 0
for idx, row in df_art.iterrows():
    cod = s(row.get('Codice'))
    if not cod: continue
    
    doc_ref = db.collection('articoli').document(str(cod).replace("/", "_").replace(".", "_"))
    data = {
        "codice": cod,
        "descrizione": s(row.get('Descrizione')),
        "confezionamento": s(row.get('Confezionamento')),
        "unita_principale": s(row.get('Unit principale')) or s(row.get('Unita principale')),
        "per": s(row.get('Per')),
        "unita_secondaria": s(row.get('Unit secondaria')) or s(row.get('Unita secondaria')),
        "ratio": s(row.get('Ratio')),
        "porzioni_unita": s(row.get('Porzioni/Unit')) or s(row.get('Porzioni/Unita'))
    }
    batch.set(doc_ref, data, merge=True)
    count += 1
    if count % 400 == 0:
        batch.commit()
        batch = db.batch()

batch.commit()
print(f"-> Articoli caricati! ({count} record)\n")

print("Finito!")
