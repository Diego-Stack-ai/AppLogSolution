import openpyxl
from pathlib import Path

PROG_DIR = Path(__file__).parent
MAPPATURA_XLSX = PROG_DIR / "mappatura_destinazioni.xlsx"

def check_headers(path):
    if not path.exists():
        return f"File {path.name} non trovato."
    try:
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        ws = wb.active
        headers = [cell.value for cell in ws[1]]
        wb.close()
        return headers
    except Exception as e:
        return f"Errore: {e}"

print("--- HEADERS MAPPATURA ---")
print(check_headers(MAPPATURA_XLSX))
