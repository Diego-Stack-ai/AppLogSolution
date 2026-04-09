import pandas as pd
from pathlib import Path

ROOT = Path(r'g:\Il mio Drive\AppLogSolutions')

# ── DNR ──────────────────────────────────────────────────────────────────────
print('=== DNR (mappatura_destinazioni.xlsx) ===')
df1 = pd.read_excel(
    ROOT / 'Progetto Scuole' / 'PROGRAMMA' / 'mappatura_destinazioni.xlsx',
    usecols=['Codice Frutta', 'Codice Latte', 'A chi va consegnato',
             'Latitudine', 'Longitudine', 'Stato geocoding']
)
valide1 = df1[
    df1['A chi va consegnato'].notna() &
    (df1['A chi va consegnato'].astype(str).str.strip() != '')
].copy()

con_coord = int(valide1.dropna(subset=['Latitudine', 'Longitudine']).shape[0])
senza_coord = int(valide1[valide1['Latitudine'].isna()].shape[0])

print(f'  Righe valide:       {len(valide1)}')
print(f'  Con coordinate:     {con_coord}')
print(f'  Senza coordinate:   {senza_coord}')
print(f'  Campione (prime 3):')
print(valide1.head(3).to_string())

# ── GRAN CHEF ─────────────────────────────────────────────────────────────────
print()
print('=== GRAN CHEF (Anagrafica_Clienti_Master.xlsx) ===')
df2 = pd.read_excel(
    ROOT / 'Fatturazione' / 'Anagrafica_Clienti_Master.xlsx',
    usecols=['Codice Cliente', 'Ragione Sociale', 'Indirizzo', 'Località', 'Provincia']
)

valide2 = df2[df2['Ragione Sociale'].notna()].copy()
print(f'  Righe valide:       {len(valide2)}')
print(f'  Campione (prime 3):')
print(valide2.head(3).to_string())

# ── RIEPILOGO ─────────────────────────────────────────────────────────────────
print()
print('=' * 55)
print('  TOTALE PREVISTO SU FIREBASE:')
print(f'    DNR:       {len(valide1)} documenti')
print(f'    GRAN CHEF: {len(valide2)} documenti')
print(f'    TOTALE:    {len(valide1) + len(valide2)} documenti')
print('=' * 55)
