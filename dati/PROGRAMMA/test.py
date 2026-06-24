import pandas as pd
df = pd.read_excel(r'g:\Il mio Drive\App\AppLogSolutionLocale\dati\rientri_ddt.xlsx')
lavorazione = df[df['Stato'].str.contains('lavorazione', na=False, case=False)]
print(f"Total in lavorazione: {len(lavorazione)}")
if len(lavorazione) > 0:
    print("Examples:")
    print(lavorazione[['Codice consegna', 'Data DDT', 'Stato']].head(10))
