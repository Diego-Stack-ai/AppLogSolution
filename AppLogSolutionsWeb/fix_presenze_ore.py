import firebase_admin
from firebase_admin import credentials, firestore

SERVICE_ACCOUNT_PATH = r"g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json"

cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

def parse_time(val):
    if not val or not val.strip(): return 0.0
    val = str(val).strip().replace(",", ".")
    if ":" in val:
        parts = val.split(":")
        h = int(parts[0]) if parts[0].isdigit() else 0
        m = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        return h + m / 60.0
    try:
        return float(val)
    except:
        return 0.0

docs = db.collection("presenze").stream()

count = 0
for doc in docs:
    data = doc.to_dict()
    
    valInizioM = str(data.get("oraInizioM", "")).strip()
    valFineM = str(data.get("oraFineM", "")).strip()
    valInizioP = str(data.get("oraInizioP", "")).strip()
    valFineP = str(data.get("oraFineP", "")).strip()

    if not valInizioM and not valFineM and not valInizioP and not valFineP:
        continue
        
    decInizioM = parse_time(valInizioM)
    decFineM = parse_time(valFineM)
    decInizioP = parse_time(valInizioP)
    decFineP = parse_time(valFineP)

    total_hours = 0.0

    if valInizioM and not valFineM and not valInizioP and valFineP:
        diff = decFineP - decInizioM if decFineP >= decInizioM else (24 - decInizioM) + decFineP
        if decFineP == 0 and decInizioM == 0: diff = 0
        total_hours = diff
    else:
        morn_hours = 0.0
        if valInizioM and valFineM:
            morn_hours = decFineM - decInizioM if decFineM >= decInizioM else (24 - decInizioM) + decFineM
            if decFineM == 0 and decInizioM == 0: morn_hours = 0
        aft_hours = 0.0
        if valInizioP and valFineP:
            aft_hours = decFineP - decInizioP if decFineP >= decInizioP else (24 - decInizioP) + decFineP
            if decFineP == 0 and decInizioP == 0: aft_hours = 0
        total_hours = morn_hours + aft_hours

    oreTotaliVal = data.get("oreTotali", 0)
    if total_hours > 0 and (oreTotaliVal == 0 or oreTotaliVal == "0" or oreTotaliVal == "0.00" or oreTotaliVal == 0.0):
        nome_autista = str(data.get("nomeAutista", "")).lower()
        is_diego = "diego boschetto" in nome_autista or "boschetto diego" in nome_autista
        standard_hours = 8.0 if is_diego else 8.5
        
        ordinarie = min(total_hours, standard_hours)
        straordinarie = max(0.0, total_hours - standard_hours)
        
        doc.reference.update({
            "oreTotali": total_hours,
            "oreOrdinarie": ordinarie,
            "oreStraordinarie": straordinarie
        })
        count += 1
        nome = data.get('nomeAutista', 'Unknown')
        dt = data.get('data', '')
        print(f"Updated {nome} il {dt} -> Totali: {total_hours}")

print(f"Aggiornati {count} record.")
