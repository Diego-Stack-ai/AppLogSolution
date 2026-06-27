import os
import PyPDF2
import re

pdf_dir = r"g:\Il mio Drive\App\AppLogSolutionsWeb\Fatture gennaio maggio"
results = []
totale_calcolato = 0.0

for filename in os.listdir(pdf_dir):
    if not filename.endswith(".pdf"):
        continue
    filepath = os.path.join(pdf_dir, filename)
    reader = PyPDF2.PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    doc_type = "UNKNOWN"
    doc_num = "UNKNOWN"
    imponibile = 0.0
    
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if "TD01 fattura" in line:
            doc_type = "Fattura"
            parts = line.split()
            for p in parts:
                if '/' in p and '-' not in p:
                    doc_num = p
                    break
        elif "TD04 nota di credito" in line or "nota di credito" in line.lower():
            doc_type = "Nota di credito"
            parts = line.split()
            for p in parts:
                if '/' in p and '-' not in p:
                    doc_num = p
                    break
        elif "TD0" in line:
            parts = line.split()
            for p in parts:
                if '/' in p and '-' not in p:
                    doc_num = p
                    break

    # Look for "I (esigibilità immediata)" and parse the next line
    for i, line in enumerate(lines):
        if "esigibilità immediata" in line:
            if i + 1 < len(lines):
                next_line = lines[i+1]
                # Regex to match the percentages and values
                # E.g. Iva al 22%22,00 450,50 99,11
                # E.g. Iva al 10%10,00 100,00 10,00
                m = re.search(r'%\d+,\d+\s+(\d{1,3}(?:\.\d{3})*,\d{2})\s+(\d{1,3}(?:\.\d{3})*,\d{2})', next_line)
                if m:
                    imponibile_str = m.group(1).replace('.', '').replace(',', '.')
                    imponibile = float(imponibile_str)
                    break
                else:
                    m2 = re.search(r'(\d{1,3}(?:\.\d{3})*,\d{2})\s+(\d{1,3}(?:\.\d{3})*,\d{2})', next_line)
                    if m2:
                        imponibile_str = m2.group(1).replace('.', '').replace(',', '.')
                        imponibile = float(imponibile_str)
                        break

    if "-F/" in doc_num or (doc_num == "UNKNOWN" and "-F/" in text):
        doc_type = "Autofattura"
        
    if "N" in doc_num:
        doc_type = "Nota di credito"

    results.append({
        "file": filename,
        "type": doc_type,
        "num": doc_num,
        "imponibile": imponibile
    })

# Now format the output for the artifact
with open(r"g:\Il mio Drive\App\AppLogSolutionsWeb\Fatture gennaio maggio\lista_riepilogo.md", "w", encoding="utf-8") as f:
    f.write("# Lista Documenti: Fatture Gennaio - Maggio\n\n")
    f.write("| Nome File | Numero Doc | Tipologia | Imponibile (€) | Azione |\n")
    f.write("| --- | --- | --- | --- | --- |\n")
    
    for r in sorted(results, key=lambda x: x['num']):
        azione = ""
        val = r['imponibile']
        if r['type'] == 'Fattura':
            azione = "Sommato"
            totale_calcolato += val
        elif r['type'] == 'Nota di credito':
            azione = "Sottratto"
            totale_calcolato -= val
            val = -val
        elif r['type'] == 'Autofattura':
            azione = "Escluso"
            val = 0.0
            
        f.write(f"| {r['file']} | {r['num']} | {r['type']} | {val:.2f} | {azione} |\n")
        
    f.write(f"\n**TOTALE CALCOLATO: {totale_calcolato:.2f} €**\n")
print("Riepilogo generato.")
