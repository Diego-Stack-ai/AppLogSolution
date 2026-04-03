import os
import pandas as pd

base_dir = r"g:\Il mio Drive\AppLogSolutions\Progetto Scuole\CONSEGNE"
master_file = os.path.join(base_dir, "Riepilogo_Generale_DDT_Mese.xlsx")

if not os.path.exists(master_file):
    print("Master file non trovato!")
    exit(1)

df = pd.read_excel(master_file)

# We want to group by Cartella/Data and count Latte/Frutta
grouped = df.groupby(['Cartella', 'Tipologia']).size().unstack(fill_value=0).reset_index()

# Ensure we have both columns even if zero
if 'LATTE' not in grouped.columns:
    grouped['LATTE'] = 0
if 'FRUTTA' not in grouped.columns:
    grouped['FRUTTA'] = 0

# Calculate total per day
grouped['Totale Giorno'] = grouped['LATTE'] + grouped['FRUTTA']

# Calculate total for the month
total_latte = grouped['LATTE'].sum()
total_frutta = grouped['FRUTTA'].sum()
total_overall = grouped['Totale Giorno'].sum()

# Append total row
total_row = pd.DataFrame([{
    'Cartella': 'TOTALE MESE',
    'LATTE': total_latte,
    'FRUTTA': total_frutta,
    'Totale Giorno': total_overall
}])

final_df = pd.concat([grouped, total_row], ignore_index=True)

# Save to a new Excel file
out_file = os.path.join(base_dir, "Riepilogo_Conteggio_Giornaliero_DDT.xlsx")
final_df.to_excel(out_file, index=False)

print(f"Riepilogo giornaliero creato in {out_file} con successo!")
