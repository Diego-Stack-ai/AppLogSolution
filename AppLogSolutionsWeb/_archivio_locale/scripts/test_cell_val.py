import pandas as pd
import numpy as np

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

data = {
    'Codice Partenza': ['Sommacampagna'],
    'Codice Arrivo': ['12345'],
    'Quantita': [5]
}
df = pd.DataFrame(data)
row = df.iloc[0]

print("Codice Arrivo:", _cell_val(row, "Codice arrivo", 8))
print("Codice Partenza (fallback 8 if not found):", _cell_val(row, "NonEsiste", 0))
