#!/usr/bin/env python3
import pdfplumber
import pandas as pd
import re
from pathlib import Path

# --- CONFIGURAZIONE ---
INPUT_DIR = Path(r"g:\Il mio Drive\App\AppLogSolution\dati\CONSEGNE")
OUTPUT_FILE = Path(r"g:\Il mio Drive\App\AppLogSolution\dati\analisi_codici.xlsx")

# --- ARTICOLI NOTI (SORGENTE DI VERITÀ) ---
ARTICOLI_NOTI = {
    "10-FLYER", "10-GEL", "10-MANIFESTO", "10-AT-01", "10-BICC", "10-CUCCH", "10-PIATTO",
    "AP-SU-PC", "FO-DI-PV-04-LB", "FO-DI-GP-01-NI", "FVNS-03", "FVNS-03-", 
    "LT-AQ-04-LV", "LT-AQ-04-LB", "LT-AQ-04-LS", "LT-DL-02-LC", "LT-ES-04-LS", "LT-ESL-IN-LB", 
    "MA-T-LI-L3-NA", "ME-T-DI-V0-NA", "ME-S-BI-L3-NA", "PE-T-DI-L3-NA",
    "YO-BI-MN-04-LB", "YO-DL-02-LC", "FI-Z-BI-L3-NA", "FR-M-BI-L3-NI",
    "LNS-04-GADGET", "LNS-04-", "CA-Z-BI-L3-NA", "KI-S-BI-L3-NA"
}

def is_primary_code(text):
    """Rileva se una stringa è l'inizio di un nuovo blocco articolo (RIGA 1)."""
    if not text: return False
    text = text.strip().upper()
    if text in ARTICOLI_NOTI: return True
    for prefix in ARTICOLI_NOTI:
        if prefix.endswith('-') and text.startswith(prefix):
            return True
    return False

def process_pdf(pdf_path):
    """
    Estrae i codici articolo dal PDF e li raggruppa in blocchi da 1 a 3 righe.
    """
    blocks = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    # In genere il codice è nella prima colonna (index 0)
                    if not table or not table[0]:
                        continue
                        
                    # Verifica se è la tabella dei prodotti (cerca intestazione "Cod.")
                    is_product_table = any("Cod." in str(cell) for cell in table[0] if cell)
                    start_row = 1 if is_product_table else 0
                    
                    current_block = []
                    
                    for row in tab[start_row:]:
                        if not row or not row[0]: continue
                        
                        # Estraggo e filtro le righe della cella
                        cell_content = str(row[0]).strip().split('\n')
                        filtered = [l.strip() for l in cell_content 
                                    if l.strip() and not l.strip().startswith("Codice:")]
                        
                        if not filtered: continue

                        if is_primary_code(filtered[0]):
                            # Salva blocco precedente
                            if current_block: blocks.append(current_block)
                            current_block = filtered
                        else:
                            # Accoda a blocco esistente
                            if current_block:
                                current_block.extend(filtered)
                            else:
                                current_block = filtered
                    
                    # Salva l'ultimo blocco
                    if current_block: blocks.append(current_block)
                        
    except Exception as e:
        print(f"Errore processando {pdf_path.name}: {e}")
        
    # Arricchisce i blocchi con il nome del file
    result = []
    for b in blocks:
        row_data = {
            "PDF_Filename": pdf_path.name,
            "Riga_1": b[0] if len(b) > 0 else "",
            "Riga_2": b[1] if len(b) > 1 else "",
            "Riga_3": b[2] if len(b) > 2 else ""
        }
        result.append(row_data)
    return result

def main():
    print(f"Scansione PDF in corso in: {INPUT_DIR}")
    
    # Trova tutti i PDF ricorsivamente (nei sotto-DDT originari divisi o master)
    # Cerchiamo specificamente nelle cartelle DDT-ORIGINALI-DIVISI per avere dati atomici
    pdf_files = list(INPUT_DIR.rglob("*.pdf"))
    print(f"Trovati {len(pdf_files)} file PDF da analizzare.")
    
    # Analisi TOTALE come richiesto
    total = len(pdf_files)
    all_data = []
    
    # Utilizziamo il multiprocessing per velocizzare drasticamente l'analisi dei 2600+ file
    from concurrent.futures import ProcessPoolExecutor, as_completed
    import os
    
    # Numero di processori da usare (lasciamo un core libero per stabilità)
    max_workers = max(1, os.cpu_count() - 1)
    print(f"Avvio elaborazione parallela su {max_workers} core...")

    count = 0
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Sottomettiamo tutti i compiti
        futures = {executor.submit(process_pdf, pdf): pdf for pdf in pdf_files}
        
        for future in as_completed(futures):
            count += 1
            if count % 10 == 0:
                print(f"Avanzamento: {count}/{total} file processati ({(count/total)*100:.1f}%)")
            
            try:
                data = future.result()
                all_data.extend(data)
            except Exception as e:
                pdf_name = futures[future].name
                print(f"Errore critico su {pdf_name}: {e}")

    if not all_data:
        print("Nessun dato estratto.")
        return

    # Creazione Excel con Pandas
    print(f"Generazione Excel finale: {OUTPUT_FILE.name}")
    df = pd.DataFrame(all_data)
    
    # Rimuovi eventuali duplicati esatti per pulire l'analisi (stesso codice nello stesso rigo)
    # È normale che lo stesso codice appaia in PDF diversi
    df = df.drop_duplicates(subset=["PDF_Filename", "Riga_1", "Riga_2", "Riga_3"])
    
    try:
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"COMPLETATO! Analisi TOTALE salvata in: {OUTPUT_FILE}")
    except Exception as e:
        print(f"Errore nel salvataggio Excel: {e}")

if __name__ == "__main__":
    main()
