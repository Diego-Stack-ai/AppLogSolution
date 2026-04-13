import pandas as pd

codes_to_find = [
    "10-AT-01",
    "10-BICC",
    "10-CUCCH",
    "10-PIATTO",
    "CA-Z-BI-L3-NA",
    "FO-DI-GP-01-NI",
    "KI-S-BI-L3-NA",
    "ME-T-DI-V0-NA",
    "PE-T-DI-L3-NA"
]

file_path = r"g:\Il mio Drive\App\AppLogSolution\dati\analisi_codici.xlsx"
df = pd.read_excel(file_path)

print(f"File caricato. Righe totali: {len(df)}")

results = {}

for code in codes_to_find:
    # Cerchiamo nelle colonne Riga_1, Riga_2, Riga_3
    mask = df['Riga_1'].str.contains(code, na=False) | \
           df['Riga_2'].str.contains(code, na=False) | \
           df['Riga_3'].str.contains(code, na=False)
    
    matches = df[mask]['PDF_Filename'].unique().tolist()
    results[code] = matches[:2] # Prendiamo solo i primi due come richiesto

print("\n--- RISULTATI RICERCA ---")
for code, ddt_list in results.items():
    if ddt_list:
        print(f"{code}: {', '.join(ddt_list)}")
    else:
        print(f"{code}: NON TROVATO")
