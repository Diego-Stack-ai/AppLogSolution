import sys
from pathlib import Path
import pdfplumber

def main():
    base_dir = Path(r"g:\Il mio Drive\App\AppLogSolutionLocale\dati\CONSEGNE")
    
    # Cerchiamo in tutte le sottocartelle CONSEGNE_*
    consegne_dirs = [d for d in base_dir.glob("CONSEGNE_*") if d.is_dir()]
    
    pdf_files = []
    for d in consegne_dirs:
        divisi_dir = d / "DDT-ORIGINALI-DIVISI"
        if divisi_dir.exists():
            pdf_files.extend(list(divisi_dir.rglob("*.pdf")))
            
    print(f"Trovati {len(pdf_files)} PDF da analizzare.")
    
    modifiche = []
    
    for i, pdf_path in enumerate(pdf_files):
        if i > 0 and i % 50 == 0:
            print(f"Analizzati {i}/{len(pdf_files)} PDF...")
            
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    if not tables: continue
                    
                    tab = next((t for t in tables if t and len(t) > 1
                                and "Cod. Articolo" in " ".join(str(c or "") for c in t[0])), None)
                    if not tab: continue
                    
                    for row in tab[1:]:
                        if not row or not row[0]: continue
                        
                        raw_codice = str(row[0])
                        righe = [l.strip() for l in raw_codice.split('\n')
                                 if l.strip() and not l.strip().startswith("Codice:")]
                                 
                        if not righe: continue
                        
                        old_base = righe[0]
                        
                        # LOGICA OPZIONE A
                        new_base = old_base
                        if len(righe) > 1 and old_base.endswith('-'):
                            # Prende la prima parola della seconda riga
                            new_base = old_base + righe[1].split()[0]
                            
                        if old_base != new_base:
                            modifiche.append({
                                'pdf': pdf_path.name,
                                'old': old_base,
                                'new': new_base,
                                'righe': righe
                            })
                            
        except Exception as e:
            pass # ignore errors

    print("\n" + "="*50)
    print(f"SIMULAZIONE COMPLETATA SU {len(pdf_files)} FILE")
    print("="*50)
    
    if not modifiche:
        print("Nessuna modifica rilevata! L'opzione A non avrebbe alcun effetto su questi PDF.")
    else:
        # Group by old/new
        from collections import defaultdict
        grouped = defaultdict(int)
        for m in modifiche:
            grouped[(m['old'], m['new'])] += 1
            
        print(f"Rilevati {len(modifiche)} casi in cui l'Opzione A cambia l'estrazione:\n")
        
        for (old, new), count in sorted(grouped.items(), key=lambda x: x[1], reverse=True):
            print(f"- {count} occorrenze: '{old}' + riga 2  ==>  '{new}'")
            
        print("\nEsempio di dettaglio raw (primi 5):")
        for m in modifiche[:5]:
            print(f"  File: {m['pdf']} | Raw: {m['righe']}")

if __name__ == "__main__":
    main()
