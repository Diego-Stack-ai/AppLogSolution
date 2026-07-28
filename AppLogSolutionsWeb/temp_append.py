import os

code_to_append = '''
@https_fn.on_call(timeout_sec=300)
def elabora_centro_costi(req: https_fn.CallableRequest) -> typing.Any:
    """
    Legge il PDF LOGCOSTOPERSONALE e salva su Firestore i dati mensili
    per ciascun dipendente.
    """
    if not req.auth:
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.UNAUTHENTICATED, message="Non autorizzato.")
    
    file_path = req.data.get("filePath")
    mese_riferimento = req.data.get("meseRiferimento") # es: "2026-07"
    
    if not file_path or not mese_riferimento:
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT, message="Parametri mancanti.")

    try:
        anno, mese_str = mese_riferimento.split("-")
        mese_index = int(mese_str) - 1  # 0 per Gennaio, 6 per Luglio
    except:
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT, message="Formato mese non valido (atteso YYYY-MM).")
        
    try:
        import pdfplumber
        import tempfile
        import os
        
        # Download from Storage
        bucket = get_bucket()
        blob = bucket.blob(file_path)
        if not blob.exists():
            raise Exception("File PDF non trovato nello Storage.")
            
        _, temp_local_filename = tempfile.mkstemp(suffix=".pdf")
        blob.download_to_filename(temp_local_filename)
        
        # Inizializza batch
        batch = db.batch()
        importati = 0
        
        with pdfplumber.open(temp_local_filename) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text: continue
                
                if "* Totale azienda *" in text:
                    continue # Ignora la pagina del totale aziendale se presente
                
                # Parsing CF e Nome
                cf = None
                nome = None
                for line in text.split('\\n'):
                    match = re.search(r'([A-Z\s\']+?)\s+([A-Z0-9]{16})\\b', line)
                    if match:
                        nome = match.group(1).strip()
                        cf = match.group(2)
                        break
                
                if not cf:
                    continue
                
                # Parse metrics
                costo_totale = 0.0
                costo_ordinario = 0.0
                costo_straordinario = 0.0
                ore_ordinarie = 0.0
                ore_straordinarie = 0.0
                
                def estrai_valore(linea, mese_idx):
                    matches = re.findall(r'-?\d{1,3}(?:\.\d{3})*,\d{2}', linea)
                    if len(matches) >= 12 and mese_idx < 12:
                        val_str = matches[mese_idx].replace('.', '').replace(',', '.')
                        return float(val_str)
                    return 0.0

                for line in text.split('\\n'):
                    if 'C O S T O   T O T A L E' in line or 'C O S T O T O T A L E' in line:
                        costo_totale = estrai_valore(line, mese_index)
                    elif 'Costo orario ordinario' in line:
                        costo_ordinario = estrai_valore(line, mese_index)
                    elif 'Costo orario straordin' in line:
                        costo_straordinario = estrai_valore(line, mese_index)
                    elif line.strip().startswith('Ordinarie..'):
                        ore_ordinarie = estrai_valore(line, mese_index)
                    elif line.strip().startswith('Straordinarie..'):
                        ore_straordinarie = estrai_valore(line, mese_index)
                
                # Salva i dati
                doc_ref = db.collection('clienti').document('DNR').collection('costi_personale').document(mese_riferimento).collection('dipendenti').document(cf)
                batch.set(doc_ref, {
                    'nome': nome,
                    'codice_fiscale': cf,
                    'costo_totale': costo_totale,
                    'costo_orario_ordinario': costo_ordinario,
                    'costo_orario_straordinario': costo_straordinario,
                    'ore_ordinarie': ore_ordinarie,
                    'ore_straordinarie': ore_straordinarie,
                    'aggiornato_il': firestore.SERVER_TIMESTAMP
                }, merge=True)
                
                importati += 1
                
        # Commit batch
        if importati > 0:
            batch.commit()
            
        # Pulisci file locale
        os.remove(temp_local_filename)
        
        # Elimina file dallo storage per pulizia
        blob.delete()
        
        return {"importati": importati, "status": "success"}

    except Exception as e:
        print(f"Errore in elabora_centro_costi: {e}")
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INTERNAL, message=str(e))
'''

with open(r'h:\Il mio Drive\App\AppLogSolutionsWeb\functions\main.py', 'a', encoding='utf-8') as f:
    f.write(code_to_append)
