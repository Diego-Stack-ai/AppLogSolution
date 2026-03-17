import pandas as pd
import json

file_path = r'g:\Il mio Drive\AppLogSolution\dati\GESTIONE.xlsx'
try:
    df = pd.read_excel(file_path, sheet_name=None)
    for sheet_name, data in df.items():
        print(f"--- Sheet: {sheet_name} ---")
        print(data.head(10))
except Exception as e:
    print(f"Error: {e}")
