import os
import glob
import pandas as pd
import re
import sys
import datetime
from datetime import timedelta

# --- MOTORE CRONOLOGICO FESTIVITÀ ---
FESTIVITA_FISSE = {
    (1, 1),   # Capodanno
    (1, 6),   # Epifania
    (4, 25),  # Liberazione
    (5, 1),   # Lavoratori
    (6, 2),   # Repubblica
    (8, 15),  # Ferragosto
    (11, 1),  # Tutti i Santi
    (12, 8),  # Immacolata
    (12, 25), # Natale
    (12, 26)  # Santo Stefano
}

def get_easter(year):
    """Calcolo della Pasqua Cattolica (Algoritmo di Gauss-Meeus)"""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    L = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * L) // 451
    month = (h + L - 7 * m + 114) // 31
    day = ((h + L - 7 * m + 114) % 31) + 1
    return datetime.date(year, month, day)

def is_holiday(date_obj):
    # Weekends (5=Sabato, 6=Domenica)
    if date_obj.weekday() >= 5:
        return True
    # Feste fisse
    if (date_obj.month, date_obj.day) in FESTIVITA_FISSE:
        return True
    # Pasquetta (Il giorno successivo a Pasqua)
    easter_sunday = get_easter(date_obj.year)
    easter_monday = easter_sunday + timedelta(days=1)
    if date_obj == easter_monday:
        return True 
    return False

def get_prossimo_giorno_lavorativo(order_date_str):
    try:
        date_obj = datetime.datetime.strptime(order_date_str, "%d/%m/%Y").date()
    except Exception:
        return order_date_str # Restituisci la stringa nuda e cruda in caso d'errore anomalo
        
    current_date = date_obj + timedelta(days=1) # 1) Assumiamo in principio il giorno DOPO
    
    # 2) "Scivolamento" automatico: Se cadiamo su una festa o sabato/domenica andiamo avanti
    while is_holiday(current_date):
        current_date += timedelta(days=1)
        
    return current_date.strftime("%d/%m/%Y")


# --- CORE SCRIPT EXTRACTOR ---
def parse_viaggio_string(s):
    match = re.search(r'del (\d{2}/\d{2}/\d{4})', s)
    return match.group(1) if match else "DataSconosciuta"

def seleziona_mese(dir_input, base_path):
    if not os.path.exists(dir_input):
        print(f"❌ ERRORE: Cartella {dir_input} non trovata.")
        sys.exit(1)
        
    subdirs = [d for d in os.listdir(dir_input) if os.path.isdir(os.path.join(dir_input, d))]
    
    if not subdirs:
        print(f"❌ ERRORE: Nessuna sottocartella trovata dentro {dir_input}.")
        sys.exit(1)

    print("\n" + "="*50)
    print(" 🗓️  SELEZIONA IL MESE DI LAVORAZIONE")
    print("="*50)
    
    sorted_subdirs = sorted(subdirs)
    for i, cartella in enumerate(sorted_subdirs, 1):
        print(f"  [{i}] {cartella.upper()}")
    print("="*50)
    
    while True:
        try:
            scelta = int(input("\nDigita il numero del mese e premi INVIO: "))
            if 1 <= scelta <= len(sorted_subdirs):
                mese_scelto = sorted_subdirs[scelta - 1]
                break
        except ValueError:
            pass
        print("❌ Scelta non valida, riprova.")
        
    config_file = os.path.join(base_path, "MESE_IN_CORSO.txt")
    with open(config_file, "w", encoding="utf-8") as f:
        f.write(mese_scelto)
        
    print(f"\n✅ Mese [{mese_scelto.upper()}] impostato! Tutti i programmi useranno questa dir.\n")
    return mese_scelto

def esegui_riepilogo(dir_input_base, dir_output_base, base_path):
    mese = seleziona_mese(dir_input_base, base_path)
    
    input_dir = os.path.join(dir_input_base, mese)
    output_dir = os.path.join(dir_output_base, mese)
    
    file_list = glob.glob(os.path.join(input_dir, "*.xlsx"))
    viaggi_per_data = {}
    
    if not file_list:
        print(f"Nessun file Excel trovato all'interno di {input_dir}")
        return
        
    for file_path in file_list:
        file_name = os.path.basename(file_path)
        if file_name.startswith('~$'):
            continue
        try:
            df_full = pd.read_excel(file_path, header=None)
            viaggio_string = "Viaggio Sconosciuto"
            data_viaggio_corretta = "DataSconosciuta"
            
            for idx, row in df_full.head(15).iterrows():
                for cell in row:
                    if isinstance(cell, str) and 'Viaggio' in cell and 'del' in cell:
                        viaggio_string = str(cell).strip()
                        data_ordine_grezza = parse_viaggio_string(viaggio_string)
                        # MAGIC SHIFT: CALCOLO DELLA REALE DATA DI CONSEGNA LAVORATIVA (D+1 ecc.)
                        if data_ordine_grezza != "DataSconosciuta":
                            data_viaggio_corretta = get_prossimo_giorno_lavorativo(data_ordine_grezza)
                        break
                if viaggio_string != "Viaggio Sconosciuto":
                    break
                    
            if data_viaggio_corretta == "DataSconosciuta":
                continue
                
            header_row_idx = -1
            for idx, row in df_full.iterrows():
                row_str = row.astype(str).str.lower().tolist()
                if any('ragione sociale' in str(c) for c in row_str):
                    header_row_idx = idx
                    break
                    
            if header_row_idx != -1:
                headers = df_full.iloc[header_row_idx].astype(str).str.strip()
                df_clienti = df_full.iloc[header_row_idx+1:].copy()
                df_clienti.columns = headers
                col_cod = 'Codice' if 'Codice' in df_clienti.columns else df_clienti.columns[0]
                df_clienti = df_clienti.dropna(subset=[col_cod])
                df_clienti = df_clienti[~df_clienti[col_cod].astype(str).str.contains('Totale', case=False, na=False)]
                cols_utili = []
                for c in df_clienti.columns:
                    cl = str(c).lower()
                    if any(x in cl for x in ['codice', 'ragione sociale', 'indirizzo', 'localita', 'località', 'pr.', 'provincia', 'colli', 'peso', 'note']):
                        cols_utili.append(c)
                if cols_utili:
                    df_clienti = df_clienti[cols_utili]
                if data_viaggio_corretta not in viaggi_per_data:
                    viaggi_per_data[data_viaggio_corretta] = []
                viaggi_per_data[data_viaggio_corretta].append({
                    "viaggio": viaggio_string,  # Conserva il nome logico originale per riferimento interno
                    "df": df_clienti,
                    "file_name": file_name
                })
        except Exception as e:
            print(f"Errore su {file_name}: {e}")
            pass
            
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for data_str, elenco_viaggi in viaggi_per_data.items():
        try:
            date_obj = datetime.datetime.strptime(data_str, "%d/%m/%Y")
            data_file_name = date_obj.strftime("%Y-%m-%d")
        except:
            data_file_name = data_str.replace("/", "-")
            
        file_output = os.path.join(output_dir, f"Riepilogo_Viaggi_{data_file_name}.xlsx")
        
        try:
            with pd.ExcelWriter(file_output, engine='openpyxl') as writer:
                foglio_name = "Riepilogo_Giornaliero"
                pd.DataFrame().to_excel(writer, sheet_name=foglio_name)
                worksheet = writer.sheets[foglio_name]
                current_row = 1
                for info in elenco_viaggi:
                    # Lasciamo la prova dell'ordine grezzo ma diamogli la data corretta in fianco volendo. Qui stampa la riga originale.
                    worksheet.cell(row=current_row, column=1, value=info["viaggio"])
                    current_row += 2
                    headers = list(info["df"].columns)
                    for col_idx, h in enumerate(headers, start=1):
                        worksheet.cell(row=current_row, column=col_idx, value=h)
                    current_row += 1
                    for idx, row_val in info["df"].iterrows():
                        for col_idx, c_val in enumerate(row_val, start=1):
                            worksheet.cell(row=current_row, column=col_idx, value=str(c_val) if pd.notna(c_val) else "")
                        current_row += 1
                    current_row += 3
            print(f"✅ Generato file post-datato operativo: {os.path.basename(file_output)}")
        except Exception as e:
            print(f"❌ File {file_output} in uso o interrotto: {e}")
            
if __name__ == "__main__":
    base = r"G:\Il mio Drive\Fatturazione"
    d_in = os.path.join(base, "File_Excel")
    d_out = os.path.join(base, "Riepiloghi_Giornalieri")
    esegui_riepilogo(d_in, d_out, base)
