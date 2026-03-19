import openpyxl
from pathlib import Path

def analyze_mapping():
    path = Path("mappatura_destinazioni.xlsx")
    if not path.exists():
        print("Mappatura non trovata.")
        return
    
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    
    addr_map = {}
    for r_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        addr = str(row[4].value or "").strip().lower()
        if addr and addr != "none":
            if addr not in addr_map: addr_map[addr] = []
            addr_map[addr].append({
                "row": r_idx, 
                "nome": str(row[2].value or ""), 
                "cod_f": str(row[0].value or ""), 
                "cod_l": str(row[1].value or "")
            })
            
    dupes = {a: info for a, info in addr_map.items() if len(info) > 1}
    print(f"--- ANALISI MAPPATURA ---")
    print(f"Indirizzi che compaiono in più righe: {len(dupes)}")
    
    for addr, info in dupes.items():
        print(f"\nIndirizzo: {addr.upper()}")
        for i in info:
            print(f"  - Riga {i['row']}: {i['nome']} (Codici: F:{i['cod_f']}, L:{i['cod_l']})")
    
    wb.close()

if __name__ == "__main__":
    analyze_mapping()
