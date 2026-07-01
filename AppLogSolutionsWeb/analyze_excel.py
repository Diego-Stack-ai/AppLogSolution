import pandas as pd

file_path = r"G:\Il mio Drive\App\AppLogSolutionsWeb\Scheda Fatturazione per Cattel.xlsx"

try:
    df_raw = pd.read_excel(file_path, sheet_name="MAGGIO", header=None)
    print("--- Sheet: MAGGIO ---")
    # Print the lower part of the sheet, e.g., from row 32 onwards
    print(df_raw.tail(20).to_string())
except Exception as e:
    print(f"Error: {e}")
