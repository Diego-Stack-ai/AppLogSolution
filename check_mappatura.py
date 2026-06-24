import openpyxl
from pathlib import Path

path = Path(r'g:\Il mio Drive\App\AppLogSolutionLocale\dati\PROGRAMMA\mappatura_destinazioni.xlsx')
wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
ws = wb.active

targets = {'p1704', 'p2357'}
print("Ricerca p1704 e p2357 in mappatura_destinazioni.xlsx:")
print(f"{'Riga':<5} {'Cod.F':<12} {'Cod.L':<12} {'Nome'}")
print('-' * 75)
for r_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
    cf = str(row[0].value or '').strip().lower()
    cl = str(row[1].value or '').strip().lower()
    nome = str(row[2].value or '').strip()[:45]
    if cf in targets or cl in targets:
        print(f"{r_idx:<5} {cf:<12} {cl:<12} {nome}")
wb.close()
print("Fine.")
