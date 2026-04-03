import os
import glob
import pandas as pd
import re
import sys
import datetime
import requests
import urllib.parse
import shutil
from datetime import timedelta

# --- CONFIGURAZIONE ---
API_KEY = "AIzaSyAHQ3HjuEEIS8bn5KMh6N3UoM6kZ2MYGL4"

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
    if date_obj.weekday() >= 5: return True
    if (date_obj.month, date_obj.day) in FESTIVITA_FISSE: return True
    easter_sunday = get_easter(date_obj.year)
    easter_monday = easter_sunday + timedelta(days=1)
    if date_obj == easter_monday: return True 
    return False

def get_prossimo_giorno_lavorativo(order_date_str):
    try:
        date_obj = datetime.datetime.strptime(order_date_str, "%d/%m/%Y").date()
    except Exception:
        return order_date_str
        
    current_date = date_obj + timedelta(days=1)
    
    while is_holiday(current_date):
        current_date += timedelta(days=1)
        
    return current_date.strftime("%d/%m/%Y")


# --- MOTORE GEOGRAFICO & VALIDAZIONE ---
def normalizza_indirizzo(indirizzo):
    if not indirizzo or pd.isna(indirizzo): return ""
    return str(indirizzo).strip().lower()

def valida_indirizzo_nuovo(cliente, ind, loc, pr):
    query_address = f"{ind}, {loc} {pr}".strip(", ")
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(query_address + ', Italia')}&key={API_KEY}"
    try:
        r = requests.get(url).json()
        if r['status'] == 'OK':
            loc_type = r['results'][0]['geometry']['location_type']
            formatted = r['results'][0].get('formatted_address', '')
            if loc_type == 'APPROXIMATE':
                return False, f"APPROSSIMATIVO ({formatted})"
            return True, "OK"
        else:
            return False, f"NON TROVATO ({r['status']})"
    except Exception as e:
        return False, f"ERRORE API ({e})"

def filtra_e_valida_anagrafica(tutti_i_clienti_estratti, base_path):
    anagrafica_file = os.path.join(base_path, "Anagrafica_Clienti_Master.xlsx")
    if not os.path.exists(anagrafica_file):
        print(f"❌ ERRORE CRITICO: {anagrafica_file} non trovato. Impossibile procedere.")
        return False
        
    df_master = pd.read_excel(anagrafica_file)
    
    # Controlliamo quali colonne ha. Se 'Indirizzo' manca fa eccezione, gestiamola
    col_ind = 'Indirizzo' if 'Indirizzo' in df_master.columns else df_master.columns[2]
    
    master_indirizzi_norm = set(df_master[col_ind].apply(normalizza_indirizzo).dropna().tolist())
    
    indirizzi_da_aggiungere = []
    errori_indirizzi = []
    
    clienti_unici = {}
    for c in tutti_i_clienti_estratti:
        key = normalizza_indirizzo(c['ind'])
        if key not in clienti_unici:
            clienti_unici[key] = c
            
    print(f"\n🔍 Avvio Verifica Indirizzi su Google Maps per i NUOVI clienti rilevati...")
    
    nuovi_validi = False
    
    for key, c in clienti_unici.items():
        if key and key not in master_indirizzi_norm:
            print(f"   ❓ Nuovo indirizzo rilevato: {c['ind']} ({c['loc']}) - Controllo Google...")
            esito_ok, msg = valida_indirizzo_nuovo(c['rs'], c['ind'], c['loc'], c['pr'])
            
            if esito_ok:
                print(f"      ✅ Validato! Verrà aggiunto al Master.")
                indirizzi_da_aggiungere.append({
                    'Codice Cliente': c.get('codice', ''),
                    'Ragione Sociale': c['rs'],
                    'Indirizzo': c['ind'],
                    'Località': c['loc'],
                    'Provincia': c['pr']
                })
                master_indirizzi_norm.add(key)
                nuovi_validi = True
            else:
                print(f"      ❌ Errore Google: {msg}")
                errori_indirizzi.append({
                    'File Origine': c['file_name'],
                    'Cliente': c['rs'],
                    'Indirizzo Rilevato': c['ind'],
                    'Localitá': c['loc'],
                    'Provincia': c['pr'],
                    'Motivo Blocco': msg
                })

    if errori_indirizzi:
        df_err = pd.DataFrame(errori_indirizzi)
        err_file = os.path.join(base_path, "Indirizzi_Sconosciuti_o_Errati.xlsx")
        df_err.to_excel(err_file, index=False)
        print("\n" + "!"*60)
        print("⛔ PROCEDURA BLOCCATA: RILEVATI INDIRIZZI INAPPROPRIATI ⛔")
        print(f"Ho trovato {len(errori_indirizzi)} indirizzi non esatti. Creato il report:")
        print(f" -> {err_file}")
        print("Sistemare gli esatti indirizzi aprendo MANUALMENTE Anagrafica Clienti Master, dopodichè rilanciare lo script.")
        print("La cartella parziale del mese è stata cancellata e ripristinata a zero per sicurezza.")
        print("!"*60)
        return False
        
    if nuovi_validi:
        df_novi = pd.DataFrame(indirizzi_da_aggiungere)
        df_master = pd.concat([df_master, df_novi], ignore_index=True)
        df_master.to_excel(anagrafica_file, index=False)
        print(f"💾 Aggiornata Anagrafica Master con {len(indirizzi_da_aggiungere)} nuovi clienti sicuri!")
        
    return True


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
    
    # Raccoglitore indirizzi per fase Validazione
    tutti_indirizzi_del_giorno = []
    
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
                
                # Raccogliamo per la validazione pre-generazione
                for idx_df, r in df_clienti.iterrows():
                    def get_val(nomi_possibili):
                        for c in df_clienti.columns:
                            if str(c).lower() in nomi_possibili:
                                val = r[c]
                                return str(val).strip() if pd.notna(val) else ""
                        return ""
                    
                    codice = get_val(['codice'])
                    rs = get_val(['ragione sociale'])
                    ind = get_val(['indirizzo'])
                    loc = get_val(['località', 'localita'])
                    pr = get_val(['pr.', 'provincia'])
                    
                    if ind and ind.lower() != 'non disponibile':
                        tutti_indirizzi_del_giorno.append({
                            'codice': codice, 'rs': rs, 'ind': ind, 'loc': loc, 'pr': pr, 'file_name': file_name
                        })
                
                if data_viaggio_corretta not in viaggi_per_data:
                    viaggi_per_data[data_viaggio_corretta] = []
                viaggi_per_data[data_viaggio_corretta].append({
                    "viaggio": viaggio_string,
                    "df": df_clienti,
                    "file_name": file_name
                })
                
        except Exception as e:
            print(f"Errore su {file_name}: {e}")
            pass

    # 🔥 LANCIO FASE DI VERIFICA 🔥
    if not filtra_e_valida_anagrafica(tutti_indirizzi_del_giorno, base_path):
        # Se c'è errore: ELIMINAZIONE della cartella riepilogo a metà!
        if os.path.exists(output_dir):
            try:
                shutil.rmtree(output_dir)
                print(f"🧹 Cartella ({output_dir}) rimossa in sicurezza.")
            except Exception as e:
                print(f"🧹 Errore rimozione cartella: {e}")
        sys.exit(1) # Esce immediatamente

    # Se passa la verifica, scrive davvero le cartelle!
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
