# Estrazione dati dal PDF DDT – A chi va consegnato

Documentazione su come il programma preleva i dati dai PDF DDT e determina **a chi va consegnato** (destinatario, indirizzo, zona, orari).

---

## 1. Struttura del PDF DDT

Ogni pagina DDT contiene blocchi di testo con:
- **Data DDT**: "del dd/mm/yyyy"
- **Luogo di destinazione**: codice tipo `p2731`, `p4848` (p + 4 o 5 cifre)
- **CAUSALE DEL TRASPORTO**: codice zona (es. A3101, P3101) con eventuali orari (H10, 730, 800)
- **Destinatario**: nome scuola/ente (riga dopo "Luogo di destinazione")
- **Indirizzo**: riga successiva al destinatario
- **CAP, Città, Provincia**: nel blocco indirizzo (es. "46030 Pomponesco (MN)")

---

## 2. Dati estratti e dove

| Dato | Come viene estratto | Utilizzo |
|------|---------------------|----------|
| **Data DDT** | Regex `del\s+(\d{2})/(\d{2})/(\d{4})` | Nome cartelle, file |
| **Codice luogo** | Regex `[Ll]uogo [Dd]i [Dd]estinazione:\s*(p\d{4,5})` | Identifica la consegna, abbinamento frutta/latte |
| **Zona/Territorio** | Dopo "conto di" o "ordine e conto di": `([A-Z]\d{4})` (es. A3101 → 3101) | Raggruppamento DDT per giri |
| **Destinatario** | Riga **subito dopo** la riga che contiene "Luogo di destinazione" | Mappatura, nuovi codici |
| **Indirizzo** | Riga **due righe dopo** "Luogo di destinazione" | Mappatura, geocoding |
| **CAP** | Ultimo numero a 5 cifre prima della provincia | Mappatura |
| **Città** | Testo prima di "(XX)" provincia | Mappatura |
| **Provincia** | Regex `\(([A-Z]{2})\)` (es. VE, PD, VI) | Zona, esclude (MN) di Pomponesco (indirizzo DNR) |
| **Orario min** | Numero 3 cifre nella causale (730→07:30, 800→08:00) | Mappatura colonna M |
| **Orario max** | H10, H09 nella causale → 10:00, 09:00 (default 14:00) | Mappatura colonna N |

---

## 3. Funzioni di estrazione (crea_distinta_magazzino.py)

### `_estrai_dati_consegna_da_testo(text, codice)`
Estrae **destinatario, indirizzo, CAP, città, provincia** da una pagina:

1. Cerca "Luogo di destinazione" e usa un blocco di ~650 caratteri
2. **Destinatario**: riga successiva a quella con "Luogo di destinazione: pXXXX"
3. **Indirizzo**: riga successiva al destinatario
4. **Provincia**: prima occorrenza di `(XX)` escludendo (MN) se vicino a "Pomponesco" o "46030"
5. **CAP**: ultimo numero a 5 cifre prima della provincia
6. **Città**: testo tra CAP e provincia

### `_estrai_dati_consegna_per_codice(pdf_paths, codice)`
Cerca in tutti i PDF una pagina con `destinazione: {codice}` e applica `_estrai_dati_consegna_da_testo`.

### `_estrai_luogo_territorio(text)`
- **Luogo**: da `LUOGO_RE` (p####)
- **Territorio**: dalla sezione "CAUSALE DEL TRASPORTO", dopo "conto di" / "ordine e conto di" → cifre 2–5 (es. A3101 → 3101)

### `_estrai_causale_provincia(text)`
- **Causale**: A3101, P3101, ecc.
- **Provincia**: come sopra, con esclusione (MN) per indirizzo DNR.

---

## 4. Mappatura destinatario

La **mappatura_destinazioni.xlsx** contiene:
- **Colonna A**: Codice Frutta (p####)
- **Colonna B**: Codice Latte (p####)
- **Colonna C**: A chi va consegnato (nome scuola) – allineato da `allinea_nomi_mappatura.py`
- **Colonne D–N**: Indirizzo, CAP, città, provincia, orari, ecc.

I dati "a chi va consegnato" provengono dai PDF tramite `_estrai_dati_consegna_da_testo` e vengono usati per:
- `nuovi_codici_consegna.xlsx` (codici non in mappatura)
- Allineamento nomi nelle mappature da aggiustare
- Geocoding degli indirizzi

---

## 5. Note

- La **sezione causale** è limitata a ~150 caratteri dopo "CAUSALE DEL TRASPORTO" per evitare falsi match.
- **Pomponesco (MN)** viene escluso come provincia destinazione (è l’indirizzo DNR).
- I codici luogo sono normalizzati in **minuscolo** (p2731).
- Il **territorio** usato per i giri è sempre le cifre della causale (3101, 3107, ecc.).
