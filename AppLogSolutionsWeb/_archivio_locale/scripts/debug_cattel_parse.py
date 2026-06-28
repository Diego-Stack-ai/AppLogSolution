import sys
sys.path.append('g:\\Il mio Drive\\App\\AppLogSolutionsWeb\\functions')
import main
from firebase_admin import storage
import pandas as pd
import io

def test():
    bucket = storage.bucket(main.BUCKET_NAME)
    blob = bucket.blob('input_pdf_fornitore/CATTEL_27-06-2026_ReportPianificazione__1_.xlsx')
    file_bytes = blob.download_as_bytes()
    
    f_io = io.BytesIO(file_bytes)
    xl = pd.ExcelFile(f_io)
    
    riepilogo_name = next((s for s in xl.sheet_names if s.lower() == "riepilogo"), None)
    if not riepilogo_name:
        print("Nessun foglio riepilogo!")
        return
        
    df_riep = xl.parse(riepilogo_name)
    df_riep_clean = df_riep.dropna(how='all')
    
    header_row_idx = None
    for idx, row in df_riep_clean.iterrows():
        row_vals = [str(val).strip().lower() for val in row.values if pd.notna(val)]
        if any('codice partenza' in rv for rv in row_vals) or any('targa' in rv for rv in row_vals):
            header_row_idx = idx
            print(f"Trovato header riga {idx}: {row_vals}")
            break
            
    if header_row_idx is not None:
        df_cols = [str(val).strip() for val in df_riep_clean.loc[header_row_idx].values]
        df_data_riep = df_riep_clean.loc[header_row_idx + 1:].copy()
        df_data_riep.columns = df_cols
    else:
        print("Header non trovato!")
        df_data_riep = df_riep_clean
        
    print(f"Colonne estratte: {list(df_data_riep.columns)}")
    
    def _cell_val(row_data, col_name, fallback_idx=None):
        lower_col = str(col_name).lower()
        matched_key = next((k for k in row_data.index if str(k).lower() == lower_col), None)
        if matched_key is not None:
            val = row_data[matched_key]
        elif fallback_idx is not None and len(row_data) > fallback_idx:
            val = row_data.iloc[fallback_idx]
        else:
            return ""
        return str(val).strip() if pd.notna(val) and str(val).strip() not in ("", "nan") else ""

    deliveries_list = []
    for idx, row in df_data_riep.iterrows():
        targa = _cell_val(row, "Targa", 2)
        codice = main.clean_client_code(_cell_val(row, "Codice arrivo", 8))
        print(f"Riga {idx} -> Targa: {targa} | Codice: {codice}")
        
        if not codice or codice.lower() in ('codice arrivo', 'codicearrivo', 'sommacampagna'):
            continue
            
        deliveries_list.append(codice)
        if len(deliveries_list) > 10:
            break
            
    print(f"Deliveries list: {deliveries_list}")

if __name__ == "__main__":
    test()
