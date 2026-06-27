import PyPDF2
import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def seleziona_file():
    root = tk.Tk()
    root.withdraw() # Nasconde la finestra principale
    file_path = filedialog.askopenfilename(
        title="1. Seleziona il PDF dei Cedolini Mensili",
        filetypes=[("File PDF", "*.pdf")]
    )
    return file_path

def seleziona_cartella(titolo):
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(
        title=titolo
    )
    return folder_path

def main():
    print("Seleziona il PDF da dividere dalla finestra che si aprirà...")
    pdf_path = seleziona_file()
    
    if not pdf_path:
        print("Nessun file selezionato. Uscita.")
        return
        
    print(f"File selezionato: {pdf_path}")
    print("\nOra seleziona la cartella di destinazione dove salvare i cedolini divisi...")
    
    output_dir = seleziona_cartella("2. Seleziona la cartella di destinazione")
    if not output_dir:
        print("Nessuna cartella di destinazione selezionata. Uscita.")
        return
        
    print(f"Cartella di destinazione: {output_dir}")
    print("\nElaborazione in corso... Attendi...")

    try:
        pdf_reader = PyPDF2.PdfReader(pdf_path)
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile leggere il file PDF: {e}")
        return

    general_pages = []
    pages_by_name = {}

    for i in range(len(pdf_reader.pages)):
        text = pdf_reader.pages[i].extract_text()
        
        lines = text.split('\n')
        name = None
        for line in lines:
            # Cerchiamo la riga col nome che solitamente inizia con molti spazi e finisce con il nome in maiuscolo
            match = re.search(r'^\s{40,}([A-Z\s\']{5,})$', line.replace('\r', ''))
            if match and 'CEDOLONE' not in match.group(1) and 'Cnel' not in match.group(1):
                name = match.group(1).strip()
                break
                
        if name:
            if name not in pages_by_name:
                pages_by_name[name] = []
            pages_by_name[name].append(i)
        else:
            general_pages.append(i)

    # Crea PDF singoli per dipendente
    conteggio_dipendenti = 0
    for name, page_indices in pages_by_name.items():
        writer = PyPDF2.PdfWriter()
        for idx in page_indices:
            writer.add_page(pdf_reader.pages[idx])
        
        safe_name = name.title().replace('/', '_').replace('\\', '_').strip()
        out_file = os.path.join(output_dir, f'{safe_name}.pdf')
        
        with open(out_file, 'wb') as f:
            writer.write(f)
        print(f"Salvato: {safe_name}.pdf ({len(page_indices)} pagine)")
        conteggio_dipendenti += 1

    # Raggruppa i rimanenti nel PDF Generali
    if general_pages:
        writer = PyPDF2.PdfWriter()
        for idx in general_pages:
            writer.add_page(pdf_reader.pages[idx])
            
        out_file = os.path.join(output_dir, 'Generali.pdf')
        with open(out_file, 'wb') as f:
            writer.write(f)
        print(f"Salvato: Generali.pdf ({len(general_pages)} pagine)")

    msg = f"Operazione completata con successo!\n\nGenerati {conteggio_dipendenti} PDF dipendenti."
    if general_pages:
        msg += f"\nInoltre è stato creato 'Generali.pdf' con le restanti {len(general_pages)} pagine riassuntive."
        
    print("\nFINITO!")
    messagebox.showinfo("Completato", msg)

if __name__ == "__main__":
    main()
