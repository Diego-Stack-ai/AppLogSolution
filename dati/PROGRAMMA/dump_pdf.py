import sys
from pathlib import Path
from pypdf import PdfReader

def dump_pdf():
    pdf_path = Path(r"g:\Il mio Drive\App\AppLogSolution\dati\DDT LATTE 20-04.pdf")
    reader = PdfReader(pdf_path)
    with open("latte_dump.txt", "w", encoding="utf-8") as f:
        for page_num, page in enumerate(reader.pages):
            f.write(f"--- PAGE {page_num} ---\n")
            f.write(page.extract_text() or "")
            f.write("\n")
    print("Dump salvato in latte_dump.txt")

if __name__ == "__main__":
    dump_pdf()
