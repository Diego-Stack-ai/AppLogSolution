import sys
import re

filepath = r"G:\Il mio Drive\App\AppLogSolutionsWeb\functions\main.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target = """        # Aggiorna database e timestamp
        doc_ref.update({
            "punti_ottimizzati": punti_finali,"""

injection = """        # Aggiorna JSON in Storage per la mappa_zone
        try:
            data_str = viaggio.get("data_lavoro") or viaggio.get("data")
            if data_str:
                data_consegna = data_str.replace("/", "-")
                json_path = f"REPORTS/{data_consegna}/viaggi_giornalieri_Johnson.json"
                json_blob = bucket.blob(json_path)
                if json_blob.exists():
                    import json
                    raw_json = json.loads(json_blob.download_as_string().decode('utf-8'))
                    if isinstance(raw_json, dict):
                        zone_list = raw_json.get("zone", [])
                    else:
                        zone_list = raw_json
                        
                    modificato_json = False
                    id_zona_str = viaggio_id.split('_', 1)[1] if '_' in viaggio_id else viaggio_id
                    for z in zone_list:
                        if z.get("id_zona") == id_zona_str:
                            z["lista_punti"] = punti_finali
                            modificato_json = True
                            break
                            
                    if modificato_json:
                        json_blob.upload_from_string(json.dumps(raw_json, indent=2), content_type='application/json')
                        print(f"Aggiornato JSON Storage per {viaggio_id}")
        except Exception as json_err:
            print(f"Errore aggiornamento JSON Storage: {json_err}")

        # Aggiorna database e timestamp
        doc_ref.update({
            "punti_ottimizzati": punti_finali,"""

content = content.replace(target, injection)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
