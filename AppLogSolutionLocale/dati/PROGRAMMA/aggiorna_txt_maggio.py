import os
from pathlib import Path

PROG_DIR = Path(r"g:\Il mio Drive\App\AppLogSolutionLocale\dati\PROGRAMMA")
CONSEGNE_DIR = PROG_DIR.parent / "CONSEGNE"

def main():
    print("Inizio aggiornamento file TXT per le cartelle di Maggio...")
    
    # 1. Trova le cartelle del mese di Maggio
    cartelle_maggio = []
    for d in CONSEGNE_DIR.iterdir():
        if d.is_dir() and d.name.startswith("CONSEGNE_") and ("-05-2026" in d.name):
            cartelle_maggio.append(d)
            
    cartelle_maggio.sort(key=lambda x: x.name)
    
    for cartella in cartelle_maggio:
        data_str = cartella.name.replace("CONSEGNE_", "")
        mappe_dir = cartella / "MAPPE_MOBILE_WHATSAPP"
        txt_file = mappe_dir / "LINK_WHATSAPP_AUTISTI.txt"
        
        if not mappe_dir.exists():
            continue
            
        print(f"Aggiorno {cartella.name}...")
        
        # Genera il nuovo contenuto del file TXT
        txt_content = f" LINK MAPPE PER AUTISTI ({data_str})\n------------------------------------------\n\n"
        
        # Ordina i file HTML alfabeticamente in modo che V01 venga prima di V02
        html_files = sorted(list(mappe_dir.glob("*.html")), key=lambda x: x.name)
        
        for html_file in html_files:
            # Assicuriamoci che stiamo usando il nome con la data
            if data_str in html_file.name:
                nome_finale = html_file.name
            else:
                nome_finale = html_file.name.replace(".html", f"_{data_str}.html")
                
            v_id = html_file.name.split("_")[0]  # Es. "V01"
            
            firebase_link = f"https://log-solution-60007.web.app/mappe_autisti/{nome_finale}"
            txt_content += f"🏎️ {v_id} (MAPPA): {firebase_link}\n\n"
            
        # Scrivi il file sovrascrivendo il vecchio
        txt_file.write_text(txt_content, encoding="utf-8")
        print(f"  OK: Aggiornati i link in {txt_file.name}")

    print("\nAggiornamento completato con successo!")

if __name__ == "__main__":
    main()
