import os
import io
import time
import psutil
from legacy_parser_adapter import processa_pdf_in_memoria

def create_mock_pdf(num_pages: int) -> bytes:
    """Crea un PDF dummy in memoria usando reportlab o pypdf.
    Qui usiamo un approccio base, ma se abbiamo reportlab possiamo disegnare testo.
    Dal momento che usiamo pdfplumber per *estrarre* testo, dobbiamo creare
    un PDF con del testo reale."""
    import io
    from reportlab.pdfgen import canvas
    
    packet = io.BytesIO()
    can = canvas.Canvas(packet)
    for i in range(num_pages):
        can.drawString(10, 800, f"DDT N. 100{i} del 14/05/2026")
        can.drawString(10, 780, f"Luogo di destinazione: P0{1000 + i % 10}")
        can.drawString(10, 760, "Indirizzo: Via Roma 1")
        can.drawString(10, 740, "36000 Vicenza (VI)")
        can.drawString(10, 720, "Causale del trasporto: ordine e conto di A1234 H08 090")
        can.showPage()
    can.save()
    packet.seek(0)
    return packet.read()

def run_simulation():
    print("="*60)
    print("SIMULAZIONE ESTRAZIONE CLOUD RUN")
    print("="*60)
    
    try:
        import reportlab
    except ImportError:
        print("Installare reportlab per il test: pip install reportlab")
        return
        
    db_mappati = {
        "P01000": {"om": "08:00", "oM": "14:00"},
        "P01001": {"om": "07:00", "oM": "13:00"}
    }
    
    test_cases = [10, 50, 150] # Pagine
    
    for pages in test_cases:
        print(f"\nGenerazione Mock PDF FRUTTA di {pages} pagine...")
        pdf_bytes = create_mock_pdf(pages)
        
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024
        
        print(f"Avvio parsing in memoria (Memoria iniziale: {mem_before:.2f} MB)...")
        start = time.time()
        
        risultato = processa_pdf_in_memoria(pdf_bytes, "FRUTTA", db_mappati)
        
        elapsed = time.time() - start
        mem_after = process.memory_info().rss / 1024 / 1024
        
        print(f"--- RISULTATI ({pages} pag) ---")
        print(f"Tempo esecuzione: {elapsed:.2f} sec")
        print(f"Memoria finale:   {mem_after:.2f} MB (Delta: {mem_after - mem_before:.2f} MB)")
        print(f"PDF splittati:    {len(risultato['split_files'])}")
        print(f"Nuovi Clienti:    {len(risultato['nuovi_dati'])}")
        print(f"Deliveries ext:   {len(risultato['deliveries'])}")

if __name__ == "__main__":
    run_simulation()
