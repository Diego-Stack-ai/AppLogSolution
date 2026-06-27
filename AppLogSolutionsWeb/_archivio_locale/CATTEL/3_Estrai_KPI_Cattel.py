import sys
import os
from playwright.sync_api import sync_playwright

def main():
    print("==================================================")
    print("--- ROBOT ESTRAZIONE KPI CATTEL (STATISTICHE) ---")
    print("==================================================")
    
    if len(sys.argv) > 2:
        data_inizio = sys.argv[1]
        data_fine = sys.argv[2]
        print(f"Date fornite via argomento: {data_inizio} - {data_fine}")
    else:
        data_inizio = input("Inserisci la DATA DA (es. 01/06/2026): ").strip()
        data_fine = input("Inserisci la DATA A (es. 01/06/2026): ").strip()
        
    if not data_inizio or not data_fine:
        print("Date non valide. Uscita in corso.")
        return
        
    print("Avvio del robot (modalità VISIBILE)... attendere.")
    
    with sync_playwright() as p:
        # Avvia Chromium in modalità visibile
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
            page.locator("input[type='text']").first.fill("cattel.somma")
            page.locator("input[type='password']").first.fill("HuhN28ci")
            
            # Clic sul bottone di login
            page.locator("button[type='submit']").click()
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(2000)
            
            print("2. Navigazione verso Statistiche...")
            page.screenshot(path="debug_statistiche_prima_del_click.png")
            with open("debug_statistiche_prima_del_click.html", "w", encoding="utf-8") as f:
                f.write(page.content())
                
            try:
                page.locator("text=Statistiche").first.click(timeout=10000)
            except Exception as click_err:
                print(f"   Impossibile cliccare su Statistiche: {click_err}")
                
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(2000)
            
            print(f"3. Inserimento date: DA {data_inizio} A {data_fine}...")
            # Facciamo uno screenshot prima di provare a inserire le date per vedere come è fatta la pagina
            page.screenshot(path="debug_statistiche.png")
            with open("debug_statistiche.html", "w", encoding="utf-8") as f:
                f.write(page.content())
                
            try:
                data_da = page.locator("label:has-text('Data da') + span input")
                data_a = page.locator("label:has-text('Data a') + span input")
                
                # Svuota i campi e inserisci la data
                data_da.first.clear()
                data_da.first.fill(data_inizio)
                page.wait_for_timeout(500)
                
                data_a.first.clear()
                data_a.first.fill(data_fine)
                page.wait_for_timeout(500)
                
                # Chiudiamo il calendario e ci spostiamo premendo TAB 3 volte
                print("   Mi sposto con il tasto TAB verso il pulsante Visualizza...")
                page.keyboard.press("Tab")
                page.wait_for_timeout(300)
                page.keyboard.press("Tab")
                page.wait_for_timeout(300)
                page.keyboard.press("Tab")
                page.wait_for_timeout(300)
                
                # Ora che siamo sul pulsante, premiamo INVIO
                print("4. Premo INVIO sul pulsante Visualizza e attendo il caricamento...")
                page.keyboard.press("Enter")
                page.wait_for_timeout(5000)
                
                print("5. Cerco il pulsante di Esportazione e scarico il file...")
                # Aspettiamo il download
                with page.expect_download(timeout=60000) as download_info:
                    # Cerchiamo pulsanti che contengono Esporta o Excel
                    try:
                        page.locator("span.ui-button-text", has_text="Esporta").first.click(timeout=3000)
                    except:
                        try:
                            page.locator("span.ui-button-text", has_text="Excel").first.click(timeout=3000)
                        except:
                            page.locator(".pi-file-excel").first.click()
                
                download = download_info.value
                
                # Salvataggio file
                download_dir = r"G:\Il mio Drive\Fatturazione\CATTEL"
                os.makedirs(download_dir, exist_ok=True)
                download_path = os.path.join(download_dir, "KPI Report.xlsx")
                
                # Se esiste già un KPI Report, lo rimuoviamo per sovrascriverlo
                if os.path.exists(download_path):
                    os.remove(download_path)
                    
                download.save_as(download_path)
                print(f"   SUCCESSO! File KPI salvato in: {download_path}")
                
            except Exception as e:
                print(f"   ERRORE durante l'operazione automatica: {e}")
                print("   Lascio aperto il browser così puoi controllare cos'è andato storto o farlo a mano.")
                
            print("\n==================================================")
            print("   ELABORAZIONE COMPLETATA.")
            print("==================================================")
            
            # Aspettiamo input dall'utente per chiudere
            input("\nPREMI INVIO QUI QUANDO VUOI CHIUDERE IL BROWSER E USCIRE...")
            
        except Exception as err:
            print(f"\nERRORE DURANTE L'ESECUZIONE: {err}")
            input("Premi INVIO per uscire...")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Errore fatale: {e}")
        input("Premi INVIO per chiudere la finestra...")
