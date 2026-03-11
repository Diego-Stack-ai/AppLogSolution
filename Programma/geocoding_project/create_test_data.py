"""Genera dataset di prova input_addresses.xlsx (5-10 indirizzi reali in Italia)."""
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Indirizzi di test reali (Parma, Bologna, Modena)
addresses = [
    {"street": "Via della Repubblica", "house_number": "1", "postal_code": "43121", "city": "Parma", "province": "PR", "destination_name": "Palazzo della Pilotta"},
    {"street": "Piazza Maggiore", "house_number": "1", "postal_code": "40124", "city": "Bologna", "province": "BO", "destination_name": "Palazzo Comunale"},
    {"street": "Via Emilia", "house_number": "282", "postal_code": "41121", "city": "Modena", "province": "MO", "destination_name": "Palazzo Ducale"},
    {"street": "Strada della Repubblica", "house_number": "28", "postal_code": "43121", "city": "Parma", "province": "PR", "destination_name": "Teatro Regio"},
    {"street": "Via dell'Indipendenza", "house_number": "44", "postal_code": "40126", "city": "Bologna", "province": "BO", "destination_name": "Stazione Centrale"},
    {"street": "Via Roma", "house_number": "22", "postal_code": "41121", "city": "Modena", "province": "MO", "destination_name": "Duomo"},
    {"street": "Borgo della Salina", "house_number": "3", "postal_code": "43121", "city": "Parma", "province": "PR", "destination_name": "Museo"},
    {"street": "Via Rizzoli", "house_number": "2", "postal_code": "40125", "city": "Bologna", "province": "BO", "destination_name": "Due Torri"},
]

df = pd.DataFrame(addresses)
df.to_excel(DATA_DIR / "input_addresses.xlsx", index=False)
print(f"Creato: {DATA_DIR / 'input_addresses.xlsx'} ({len(df)} indirizzi)")
