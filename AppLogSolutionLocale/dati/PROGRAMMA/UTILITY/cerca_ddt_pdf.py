import sys
import re
from pathlib import Path
try:
    from pypdf import PdfReader
except ImportError:
    pass

def search_ddt(base_dir, query):
    base_path = Path(base_dir)
    print(f"Sto cercando '{query}'...", flush=True)
    query_lower = query.lower()
    
    pdf_files = [p for p in base_path.rglob("*.pdf") if "MASTER" not in p.name.upper() and ("DDT" in p.name.upper() or p.parent.name in ["FRUTTA", "LATTE"])]
    
    for pdf_path in pdf_files:
        try:
            reader = PdfReader(pdf_path)
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if text and query_lower in text.lower():
                    print(f"\n--> TROVATO '{query}' IN: {pdf_path.relative_to(base_path)} (Pag. {page_num})", flush=True)
                    lines = [line.strip() for line in text.split("\n") if line.strip()]
                    for i, line in enumerate(lines):
                        if query_lower in line.lower():
                            start = max(0, i-4)
                            end = min(len(lines), i+8)
                            for j in range(start, end):
                                prefix = ">> " if j == i else "   "
                                print(f"{prefix}{lines[j]}", flush=True)
                            print("-" * 40, flush=True)
                            break
        except: pass

if __name__ == "__main__":
    search_ddt(r"g:\Il mio Drive\App\AppLogSolution\dati", "p2309")
