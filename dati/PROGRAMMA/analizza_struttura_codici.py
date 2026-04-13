#!/usr/bin/env python3
import pdfplumber
import pandas as pd
import re
from pathlib import Path

# --- CONFIGURAZIONE ---
INPUT_DIR = Path(r"g:\Il mio Drive\App\AppLogSolution\dati\CONSEGNE")
OUTPUT_FILE = Path(r"g:\Il mio Drive\App\AppLogSolution\dati\analisi_codici.xlsx")

def is_new_article_code(text):
    """
    Rileva se una stringa sembra l'inizio di un nuovo codice articolo.
    Logica basata su pattern: lettere/numeri, lunghezza, trattini.
    """
    if not text:
        return False
    
    # Pattern comuni: FVNS-03-, 10-FLYER, LT-DL-02-LC, --130426
    # Inizia con almeno 2 lettere, 2 numeri o doppio trattino
    pattern = re.compile(r'^([A-Z]{2,}|[0-9]{2,}|--)')
    return bool(pattern.match(text.strip()))

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
                    
                    for row in table[start_row:]:
                        if not row or not row[0]:
                            continue
                            
                        # Estraiamo il contenuto della prima colonna (Cod. Articolo)
                        # Spesso il PDF potrebbe avere a capo nella cella stessa
                        cell_content = str(row[0]).strip().split('\n')
                        
                        for line in cell_content:
                            line = line.strip()
                            if not line:
                                continue
                                
                            if is_new_article_code(line):
                                # Se abbiamo un blocco in corso, lo salviamo prima di iniziarne uno nuovo
                                if current_block:
                                    blocks.append(current_block)
                                current_block = [line]
                            else:
                                # Se non è un nuovo codice, lo accodiamo al blocco corrente (max 3 righe)
                                if current_block:
                                    if len(current_block) < 3:
                                        current_block.append(line)
                                    else:
                                        # Se superiamo le 3 righe, chiudiamo questo e iniziamo uno nuovo
                                        # (Caso limite per evitare blocchi infiniti se la logica fallisce)
                                        blocks.append(current_block)
                                        current_block = [line]
                                else:
                                    # Caso riga orfana all'inizio
                                    current_block = [line]
                    
                    # Salva l'ultimo blocco della tabella
                    if current_block:
                        blocks.append(current_block)
                        
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
    
    all_data = []
    
    # Analizziamo un campione se sono troppi, o tutti se ragionevole
    # Per analisi strutturale, 100-200 file sono sufficienti
    count = 0
    for pdf in pdf_files:
        count += 1
        if count % 50 == 0:
            print(f"Elaborazione file {count}/{len(pdf_files)}...")
            
        # Saltiamo file master pesanti se vogliamo velocità, o analizziamo tutto
        # In questo caso analizziamo tutto per avere il quadro completo
        data = process_pdf(pdf)
        all_data.extend(data)
        
    if not all_data:
        print("Nessun dato estratto.")
        return

    # Creazione Excel con Pandas
    print(f"Generazione Excel: {OUTPUT_FILE.name}")
    df = pd.DataFrame(all_data)
    
    # Rimuovi eventuali duplicati esatti per pulire l'analisi
    df = df.drop_duplicates(subset=["Riga_1", "Riga_2", "Riga_3"])
    
    try:
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"COMPLETATO! Analisi salvata in: {OUTPUT_FILE}")
    except Exception as e:
        print(f"Errore nel salvataggio Excel: {e}")

if __name__ == "__main__":
    main()
