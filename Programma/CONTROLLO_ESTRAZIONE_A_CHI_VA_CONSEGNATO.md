# Controllo estrazione "A chi va consegnato"

Verifica di come viene estratto il campo **A chi va consegnato** (destinatario) dal PDF DDT.

---

## Differenza Frutta vs Latte

| Tipo   | Struttura dopo "Luogo di destinazione: pXXXX" |
|--------|-----------------------------------------------|
| **Frutta** | nome cliente → indirizzo                      |
| **Latte**  | **Cf** (o P.IVA) → nome cliente → indirizzo   |

Il codice **salta automaticamente** la riga Cf se riconosciuta (inizio "Cf", "C.F.", "Partita Iva", o 16 caratteri CF italiano).

---

## 1. Percorso nel codice

```
nuovi_codici_consegna.xlsx (codici non in mappatura)
    ↓
_estrai_dati_consegna_per_codice(pdf_paths, codice)
    ↓
_estrai_dati_consegna_da_testo(text, codice)
    ↓
res["destinatario"]  → colonna "A chi va consegnato"
```

**File:** `crea_distinta_magazzino.py`  
**Righe:** 508-524 (_estrai_dati_consegna_da_testo), 543-556 (_estrai_dati_consegna_per_codice)

---

## 2. Logica di estrazione

```
blocco = text[da "Luogo di destinazione" per 650 caratteri]
lines = righe del blocco (vuote e "RESPONSABILE" escluse)

Per ogni riga i che matcha LUOGO_RE ("Luogo di destinazione: pXXXX"):
    destinatario = lines[i + 1]   ← RIGA SUCCESSIVA
    indirizzo    = lines[i + 2]   ← DUE RIGHE DOPO
    break
```

**Struttura PDF attesa:**
```
Luogo di destinazione: p3123
ISTITUTO COMPRENSIVO NOME SCUOLA      ← destinatario (A chi va consegnato)
Via Roma 10, 46030 Città (VE)         ← indirizzo
...
```

---

## 3. Rischio layout diverso

Se il PDF ha una struttura diversa, l'estrazione può sbagliare:

| Caso | Cosa succede |
|------|--------------|
| Nome su 2 righe | Prende solo la prima (lines[i+1]) |
| Righe vuote tra Luogo e nome | `lines` le salta → indice sbagliato |
| "Luogo di destinazione" con testo diverso | Non matcha LUOGO_RE |
| Codice non in pagina | `codice not in text` → ritorna vuoto |
| Blocco < 650 caratteri | OK se nome e indirizzo stanno dentro |

---

## 4. Filtri applicati

```python
lines = [ln.strip() for ln in blocco.split("\n") 
         if ln.strip() and not ln.strip().upper().startswith("RESPONSABILE")]
```

- Righe vuote: **escluse**
- Righe che iniziano con "RESPONSABILE": **escluse**

Conseguenza: se tra "Luogo di destinazione" e il nome c’è una riga "RESPONSABILE...", l’indice `i+1` può puntare al nome sbagliato.

---

## 5. Verifica rapida

Per controllare l’estrazione su un PDF reale:

```python
# In Python, dalla cartella del progetto:
import pdfplumber
from pathlib import Path

pdf = list(Path("DDT frutta").glob("*.pdf"))[0]  # o "DDT latte"
with pdfplumber.open(pdf) as doc:
    text = doc.pages[0].extract_text()
    
# Cerca il blocco
idx = text.find("Luogo di destinazione")
blocco = text[idx : idx + 650]
lines = [ln.strip() for ln in blocco.split("\n") if ln.strip() and not ln.strip().upper().startswith("RESPONSABILE")]

print("=== Righe estratte (primo DDT) ===")
for i, ln in enumerate(lines[:15]):
    print(f"{i}: {ln[:60]}")
```

Se `lines[1]` non contiene il nome della scuola, la struttura del PDF non corrisponde alle assunzioni.
