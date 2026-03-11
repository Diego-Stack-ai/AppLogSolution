# Discussione: Allinea Nomi Mappatura - Nuove Direttive

## Contesto

- Il file Excel è stato ricreato dopo un problema precedente.
- Definite nuove regole per lo script `allinea_nomi_mappatura.py`.
- **Non modificare nulla** finché non si è deciso il comportamento finale.

---

## Struttura colonne Excel (A → P)

| Col | Nome colonna        | Da modificare |
|-----|---------------------|---------------|
| A   | Codice Frutta       | No            |
| B   | Codice Latte        | No            |
| C   | A chi va consegnato | **Sì**        |
| D   | Tipologia grado     | **Sì**        |
| E   | Indirizzo           | **Sì**        |
| F   | CAP                 | **Sì**        |
| G   | Città               | **Sì**        |
| H   | Provincia           | **Sì**        |
| I   | Email               | **Sì**        |
| J   | Home Page           | **Sì**        |
| K   | Tipologia consegna  | No            |
| L   | Tipologia consegna  | No            |
| M   | Email               | No            |
| N   | Sito web            | No            |
| O   | Orario min          | No            |
| P   | Orario max          | No            |

---

## Regole operative

### Colonne da modificare

- **Solo colonne C–J** (8 colonne)
- Contenuto: dati di indirizzo esatti (A chi va, Tipologia, Indirizzo, CAP, Città, Provincia, Email, Home Page)

### Colonne non toccate

- **A, B**: Codici (sempre invariati)
- **K–P**: Tipologia consegna, Email, Sito web, Orari (non modificate dallo script)

---

## Implicazioni per lo script

1. **COLS_COPIA** = colonne 3–10 (C:J in Excel, 1-based: 3, 4, 5, 6, 7, 8, 9, 10).
2. **Match** per Indirizzo, CAP, Città: colonne E (5), F (6), G (7).
3. **Nome** (A chi va): colonna C (3).
4. **Tipologia** (per fuzzy): colonna D (4).
5. **Codice**: colonna A (1) o B (2), a seconda del blocco.

---

## Domande da chiarire

1. **Righe target e sorgenti**:  
   - Target: righe 2–455?  SI qui ci sono gli indirizzi vecchi da confrontare
   - Sorgenti: righe 456+?  Si qui ci sno gli indirizzi nuovi da prendere ed incollare nelle righe 2-455

2. **File di input**:  
   - Si usa ancora `mappatura_destinazioni - da aggiustare.xlsx`? Si

3. **Fase automatica**:  
   - Mantenere la sostituzione automatica (Ind+CAP+Città 100%, Nome ≥ 90%)? Si 

4. **Duplicate**:  
   - (K, L) da lasciare – contengono dati diversi  
   - (M, N) eliminate – ora Orario min e Orario max

---

## ✅ Applicato

Lo script è stato aggiornato con la mappatura colonne C:J.
