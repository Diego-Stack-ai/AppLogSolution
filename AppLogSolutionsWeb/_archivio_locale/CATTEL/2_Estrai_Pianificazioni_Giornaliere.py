import sys
import os
import re
from datetime import datetime
from playwright.sync_api import sync_playwright
import pandas as pd

try:
    import pandas
except ImportError:
    print("ERRORE LIBRERIE MANCANTI: No module named 'pandas'")
    print("Assicurati di aver installato le librerie necessarie (es. pip install pandas playwright)")
    input("\nPremi INVIO per chiudere la finestra...")
    sys.exit(1)

def get_output_dir(data_string):
    """
    Ritorna il percorso della cartella dove salvare i file Excel, es:
    G:\\Il mio Drive\\Fatturazione\\CATTEL\\GIUGNO\\05
    """
    giorno, mese_num, anno = data_string.split('/')
    mesi = {
        '01': 'GENNAIO', '02': 'FEBBRAIO', '03': 'MARZO', '04': 'APRILE',
        '05': 'MAGGIO', '06': 'GIUGNO', '07': 'LUGLIO', '08': 'AGOSTO',
        '09': 'SETTEMBRE', '10': 'OTTOBRE', '11': 'NOVEMBRE', '12': 'DICEMBRE'
    }
    mese_nome = mesi.get(mese_num, mese_num)
    
    base_path = r"G:\Il mio Drive\Fatturazione\CATTEL"
    dir_path = os.path.join(base_path, mese_nome, giorno)
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

def main():
    print("==================================================")
    print("--- ROBOT PIANIFICAZIONI GIORNALIERE INTIME ---")
    print("==================================================")
    
    if len(sys.argv) > 2:
        data_inizio = sys.argv[1]
        data_fine = sys.argv[2]
        print(f"Date fornite via argomento: {data_inizio} - {data_fine}")
    else:
        data_inizio = input("Inserisci la DATA DA (es. 05/05/2026): ").strip()
        data_fine = input("Inserisci la DATA A (es. 05/05/2026): ").strip()
        
    if not data_inizio or not data_fine:
        print("Date non valide. Uscita in corso.")
        return
        
    data_richiesta = data_inizio # Manteniamo la variabile per compatibilità con il salvataggio cartelle
        
    output_dir = get_output_dir(data_richiesta)
    print(f"\nI dati verranno salvati nella cartella: \n{output_dir}\n")
    
    print("Avvio del robot (modalità VISIBILE)... attendere.")
    
    with sync_playwright() as p:
        # Avvia Chromium in modalità visibile per debug
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        try:
            print("1. Accesso alla pagina di Login...")
            page.goto("https://intime.lac-consulting.eu/webClient/login.xhtml")
            
            # Attende i campi
            page.wait_for_selector("input[type='text']")
            page.wait_for_selector("input[type='password']")
            
            # Inserimento credenziali
            # Selezionatori basati sul comportamento tipico di PrimeFaces/JSF
            page.locator("input[type='text']").first.fill("cattel.somma")
            page.locator("input[type='password']").first.fill("HuhN28ci")
            
            print("   Eseguo il Login...")
            # Cerca il bottone di login (solitamente ha value 'Login' o un'icona specifica)
            # Clicchiamo sul submit button
            page.locator("button[type='submit'], input[type='submit'], a:has-text('Login')").first.click()
            
            # Attendiamo che carichi la dashboard o la lista (spesso ha un menu o una tabella)
            page.wait_for_load_state('networkidle')
            
            print("2. Navigazione verso Pianificazioni...")
            # Clicca sul pulsante "Pianificazioni" invece di forzare l'URL, per evitare redirect alla home
            page.locator("text=Pianificazioni").first.click()
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(2000)
            
            print(f"3. Inserimento date: DA {data_inizio} A {data_fine} nei filtri di ricerca...")
            
            # Trova i campi Data da e Data a e inserisce la data
            try:
                # Seleziona gli input basandosi sulla loro posizione rispetto alle label
                data_da = page.locator("label:has-text('Data da') + span input")
                data_a = page.locator("label:has-text('Data a') + span input")
                
                # Svuota i campi e inserisci la data senza premere Enter per evitare refresh AJAX prematuri
                data_da.clear()
                data_da.fill(data_inizio)
                page.wait_for_timeout(500)
                
                data_a.clear()
                data_a.fill(data_fine)
                page.wait_for_timeout(500)
                
                # Chiude eventuali popup del calendario cliccando fuori (es. sul body)
                page.locator("body").click()
                page.wait_for_timeout(500)
                
                # Clicca il pulsante Aggiorna
                page.locator(".ui-button-text", has_text="Aggiorna").first.click()
                print("   Premuto Aggiorna, attendo il caricamento...")
                
            except Exception as e:
                print(f"Impossibile applicare i filtri data: {e}")
                
            # Aspettiamo che la tabella si aggiorni
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(4000)
            
            print("   Cerco la riga nella tabella aggiornata...")
            page.screenshot(path="debug_requests_table.png")
            with open("debug_requests_table.html", "w", encoding="utf-8") as f:
                f.write(page.content())
            
            # Verifichiamo se la tabella dice "Nessuna richiesta disponibile"
            if page.locator(".ui-datatable-empty-message").count() > 0 and page.locator(".ui-datatable-empty-message").is_visible():
                print("ERRORE TABELLA: La tabella mostra 'Nessuna richiesta disponibile'. I filtri potrebbero essere errati o non ci sono viaggi.")
                return

            # Gestione formati data (05 06 2026, 2026 06 05, ecc.)
            import re
            parts = data_richiesta.split('/')
            if len(parts) == 3:
                d, m, y = parts
                date_regex = re.compile(rf"({data_richiesta}|{d} {m} {y}|{y} {m} {d})")
            else:
                date_regex = re.compile(rf"({data_richiesta})")

            row_locator = page.locator("tr").filter(has_text=date_regex)
            
            if row_locator.count() == 0:
                print(f"ERRORE: La data non è stata trovata nella tabella delle pianificazioni!")
                return
                
            print("   Data trovata! Clicco sul nome della richiesta (link sottolineato) per aprire i dettagli...")
            # Clicca sul link (tag <a>) all'interno della riga, che è il "Nome" sottolineato
            row_locator.first.locator("a").first.click()
            
            # Attende il caricamento della pagina successiva (responseDetail)
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(4000)
            
            print("4. Apertura della pagina di Dettaglio Viaggi in corso...")
            
            # Aspettiamo che appaia la tabella riassuntiva dei viaggi (summary-table)
            page.wait_for_selector("tbody[id$='summary-table_data']")
            
            # Troviamo tutte le righe dei viaggi (escludendo la riga "Totale" che non ha l'attributo data-ri)
            viaggi_rows = page.locator("tbody[id$='summary-table_data'] tr[data-ri]")
            num_viaggi = viaggi_rows.count()
            print(f"Trovati {num_viaggi} viaggi per questa data.")
            
            # Ciclo su ogni viaggio
            for i in range(num_viaggi):
                row = viaggi_rows.nth(i)
                cells = row.locator("td")
                
                # Estraiamo i dati del viaggio (gli indici partono da 0)
                # In base all'analisi HTML: 2=Codice(Targa), 3=Zona, 5=Km, 6=Qta, 7=Vol, 8=Peso
                targa = cells.nth(2).inner_text().strip()
                zona_viaggio = cells.nth(3).inner_text().strip()
                km_viaggio = cells.nth(5).inner_text().strip()
                peso_viaggio = cells.nth(8).inner_text().strip()
                
                print(f"\n--- Elaborazione Viaggio {i+1}/{num_viaggi}: Targa {targa} ---")
                
                # Clicchiamo sulla cella della Targa per far caricare i clienti sotto
                print("   Clicco sulla targa per caricare i clienti...")
                cells.nth(2).click()
                
                # Attendiamo che la tabella sottostante (quella con "Committente") non mostri più "Nessun dato disponibile"
                page.wait_for_load_state('networkidle')
                page.wait_for_timeout(3000)
                
                # Troviamo la tabella dei clienti (è quella che ha la colonna "Committente")
                clienti_table = page.locator("table", has_text="Committente").last
                clienti_rows = clienti_table.locator("tbody tr")
                num_clienti = clienti_rows.count()
                
                print(f"   Trovati {num_clienti} clienti (o righe). Estrazione in corso...")
                
                clienti_data = []
                for j in range(num_clienti):
                    c_row = clienti_rows.nth(j)
                    c_cells = c_row.locator("td")
                    
                    # Evitiamo la riga "Nessun dato disponibile" se per caso appare
                    if c_cells.count() < 10:
                        continue
                        
                    # Estraiamo i dati del cliente
                    cliente = {
                        "Targa Viaggio": targa,
                        "Zona Viaggio": zona_viaggio,
                        "Km Totali Viaggio": km_viaggio,
                        "Peso Totale Viaggio": peso_viaggio,
                        "Ordine": c_cells.nth(4).inner_text().strip(),
                        "Committente": c_cells.nth(5).inner_text().strip(),
                        "Zona Cliente": c_cells.nth(6).inner_text().strip(),
                        "Zona 2": c_cells.nth(7).inner_text().strip(),
                        "Nome Cliente": c_cells.nth(8).inner_text().strip(),
                        "Indirizzo": c_cells.nth(9).inner_text().strip(),
                        "Quantità": c_cells.nth(10).inner_text().strip(),
                        "Volume": c_cells.nth(11).inner_text().strip(),
                        "Peso": c_cells.nth(12).inner_text().strip(),
                        "Fatturato": c_cells.nth(13).inner_text().strip(),
                        "Km progressivi": c_cells.nth(14).inner_text().strip(),
                    }
                    clienti_data.append(cliente)
                
                if clienti_data:
                    # Trasformiamo in un DataFrame Pandas
                    import pandas as pd
                    import os
                    df = pd.DataFrame(clienti_data)
                    
                    # Creiamo il nome del file Excel per QUESTO viaggio
                    data_file = data_richiesta.replace('/', '')
                    nome_file = f"Viaggio_{targa}_{data_file}.xlsx"
                    save_path = os.path.join(output_dir, nome_file)
                    
                    # Salvataggio
                    df.to_excel(save_path, index=False)
                    print(f"   Salvato file Excel: {nome_file} ({len(clienti_data)} clienti)")
                else:
                    print(f"   Nessun cliente valido estratto per il viaggio {targa}.")
            
            print("\n*** ESTRAZIONE COMPLETATA CON SUCCESSO! ***")
            
        except Exception as err:
            print(f"\nERRORE DURANTE L'ESECUZIONE: {err}")
            try:
                page.screenshot(path="error_debug.png")
                print("Screenshot dell'errore salvato in 'error_debug.png'")
            except:
                pass
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        input("\nPremi INVIO per chiudere la finestra...")
