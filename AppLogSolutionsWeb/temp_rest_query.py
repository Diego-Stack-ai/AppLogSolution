import requests
import json

PROJECT_ID = "log-solution-60007"

def run_query():
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents:runQuery"
    
    query = {
        "structuredQuery": {
            "from": [{"collectionId": "presenze"}],
            "where": {
                "fieldFilter": {
                    "field": {"fieldPath": "mese"},
                    "op": "EQUAL",
                    "value": {"stringValue": "2026-06"}
                }
            }
        }
    }
    
    response = requests.post(url, json=query)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return
        
    data = response.json()
    
    # Process results
    results = []
    for item in data:
        if "document" in item:
            doc = item["document"]
            fields = doc.get("fields", {})
            
            # Simple extractor
            parsed = {}
            for k, v in fields.items():
                if "stringValue" in v:
                    parsed[k] = v["stringValue"]
                elif "integerValue" in v:
                    parsed[k] = v["integerValue"]
                elif "booleanValue" in v:
                    parsed[k] = v["booleanValue"]
                elif "arrayValue" in v:
                    parsed[k] = v["arrayValue"].get("values", [])
            
            results.append(parsed)
            
    print(f"Trovati {len(results)} documenti per giugno 2026.")
    
    if len(results) > 0:
        with_tvt = sum(1 for r in results if r.get('tvt') == True or r.get('tvt') == 'true')
        with_navetta = sum(1 for r in results if r.get('navetta'))
        with_viaggio = sum(1 for r in results if r.get('viaggio'))
        with_attivita = sum(1 for r in results if r.get('attivitaAggiuntive'))
        
        print(f"Documenti con TVT: {with_tvt}")
        print(f"Documenti con Navetta: {with_navetta}")
        print(f"Documenti con Viaggio/Zona: {with_viaggio}")
        print(f"Documenti con Attività Aggiuntive: {with_attivita}")
        
        navette_viste = set(r.get('navetta') for r in results if r.get('navetta'))
        if navette_viste:
            print(f"Navette trovate: {navette_viste}")
            
if __name__ == "__main__":
    run_query()
