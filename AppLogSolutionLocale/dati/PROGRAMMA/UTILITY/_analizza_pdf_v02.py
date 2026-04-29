import pdfplumber, pathlib, re

pdf_path = pathlib.Path(r"g:\Il mio Drive\App\AppLogSolutionLocale\dati\CONSEGNE\CONSEGNE_28-04-2026\DISTINTE_VIAGGIO\DISTINTA_V02_Zone_DDT_DA_INSERIRE.pdf")

H10_RE = re.compile(r'H10\s+(\d{3,4})')  # H10 seguito dall'orario (es. H10 800 = 8:00)
CLIENT_RE = re.compile(r'Merce consegnata per ordine e conto di\s+([\w]+)', re.I)
DEST_RE = re.compile(r'Destinatario[:\s]+(.+)', re.I)
NOME_RE = re.compile(r'^(.{5,50})\s*\n', re.M)

print(f"Analisi DDT con H10 - {pdf_path.name}")
print("="*70)

trovati = {}  # pagina -> info

with pdfplumber.open(str(pdf_path)) as pdf:
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text() or ""
        m_h10 = H10_RE.search(text)
        m_cliente = CLIENT_RE.search(text)
        
        if m_h10 and m_cliente:
            codice_cliente = m_cliente.group(1).strip()
            orario_raw = m_h10.group(1)
            # Formatta orario: 800 -> 08:00, 815 -> 08:15
            h = orario_raw[:-2].zfill(2)
            m = orario_raw[-2:]
            orario = f"{h}:{m}"
            
            # Cerca nome destinatario nel testo
            linee = [l.strip() for l in text.split('\n') if l.strip()]
            nome_dest = ""
            for j, riga in enumerate(linee):
                if "Destinatario" in riga or "destinatario" in riga:
                    nome_dest = linee[j+1] if j+1 < len(linee) else ""
                    break
            
            if codice_cliente not in trovati:
                trovati[codice_cliente] = {
                    "orario": orario,
                    "nome": nome_dest,
                    "pagine": []
                }
            trovati[codice_cliente]["pagine"].append(i)

print(f"\nDDT con orario H10 trovati: {len(trovati)}\n")
for cod, info in sorted(trovati.items()):
    pagine_str = ", ".join(str(p) for p in info["pagine"])
    print(f"  Cliente: {cod:<12}  Orario: {info['orario']}  Pagine PDF: {pagine_str}")
    if info["nome"]:
        print(f"             Nome: {info['nome']}")
    print()
