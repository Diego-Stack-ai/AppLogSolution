import pdfplumber
import os
import glob

d = r'g:\Il mio Drive\App\AppLogSolution\dati\CONSEGNE\CONSEGNE_15-04-2026\DDT-ORIGINALI-DIVISI\LATTE'
pdfs = glob.glob(os.path.join(d, '*.pdf'))
found = 0

print(f"Cercando LT-DL-02-LC nei PDF della cartella {d}...")

for pdf_path in pdfs:
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                if not tables: continue
                for tab in tables:
                    if not tab or len(tab) < 2: continue
                    for row in tab:
                        if row and row[0] and 'LT-DL-02-LC' in str(row[0]):
                            print(f"\n[{os.path.basename(pdf_path)}]")
                            print(row)
                            found += 1
                            if found >= 5:
                                exit(0)
    except Exception as e:
        pass

if found == 0:
    print("Nessun articolo LT-DL-02-LC trovato nei PDF.")
