import os
import shutil
import subprocess
from pathlib import Path

PROG_DIR = Path(r"g:\Il mio Drive\App\AppLogSolutionLocale\dati\PROGRAMMA")
ROOT_DIR = PROG_DIR.parent.parent
CONSEGNE_DIR = PROG_DIR.parent / "CONSEGNE"
WEBAPP_FOLDER = ROOT_DIR / "frontend" / "mappe_autisti"

def main():
    print("Inizio ripristino storico mappe per il mese di Maggio...")
    
    # 1. Trova le cartelle del mese di Maggio
    cartelle_maggio = []
    for d in CONSEGNE_DIR.iterdir():
        if d.is_dir() and d.name.startswith("CONSEGNE_") and ("-05-2026" in d.name):
            cartelle_maggio.append(d)
            
    cartelle_maggio.sort(key=lambda x: x.name)
    
    if not cartelle_maggio:
        print("Nessuna cartella di maggio trovata.")
        return
        
    print(f"Trovate {len(cartelle_maggio)} cartelle: {[d.name for d in cartelle_maggio]}")
    
    files_copiati = 0
    
    # 2. Copia e rinomina i file
    for cartella in cartelle_maggio:
        data_str = cartella.name.replace("CONSEGNE_", "")
        mappe_dir = cartella / "MAPPE_MOBILE_WHATSAPP"
        
        if not mappe_dir.exists():
            print(f"  Saltata {cartella.name} (nessuna cartella MAPPE_MOBILE_WHATSAPP)")
            continue
            
        print(f"  Elaboro {cartella.name}...")
        
        for html_file in mappe_dir.glob("*.html"):
            # Se ha già la data nel nome (es. V01_Zone_1234_07-05-2026.html), non la aggiungiamo di nuovo
            if data_str in html_file.name:
                nuovo_nome = html_file.name
            else:
                nuovo_nome = html_file.name.replace(".html", f"_{data_str}.html")
                
            dest_file = WEBAPP_FOLDER / nuovo_nome
            shutil.copy2(html_file, dest_file)
            print(f"    -> {nuovo_nome}")
            files_copiati += 1

    print(f"\nOperazione completata. File copiati/rinominati: {files_copiati}")
    
    # 3. Deploy su Firebase
    if files_copiati > 0:
        print("\nAvvio deploy automatico su Firebase...")
        try:
            subprocess.run(["firebase", "deploy", "--only", "hosting"], cwd=ROOT_DIR, shell=True, check=True)
            print("Deploy completato con successo!")
        except Exception as e:
            print(f"Errore durante il deploy: {e}")

if __name__ == "__main__":
    main()
