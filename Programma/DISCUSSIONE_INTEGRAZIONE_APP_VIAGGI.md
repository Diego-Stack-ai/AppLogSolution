# Discussione: Integrazione App Viaggi + Distinta + Percorso

## Obiettivo generale

L'app **Gestione Viaggi** (NuovaAppPaghe) non è solo per la distinta. Serve per:
- **Autista**: inserisce orario partenza, targa mezzo, orari lavoro → ore lavorate
- **Invio dati** a Google Sheets
- **Alert**: pop-up se non ha chiuso la giornata del giorno prima

**E** si integra con la **distinta magazzino** e il **percorso di consegna**.

---

## 1. Abbinamento Distinta ↔ Autista

### Problema
Se si stampa un’unica pagina con tutte le distinte, l’autista può prendere la distinta sbagliata.

### Soluzione
- **Campo "Distinta"** nella schermata di inserimento turno
- **Dropdown** che legge le distinte disponibili (es. da cartella `Giri lavorati/DDT-[data]/RIEPILOGO/`)
- L’autista **seleziona la propria distinta** → abbinamento automatico distinta ↔ autista
- Import del **percorso** (indirizzi di consegna) dalla distinta scelta

---

## 2. Flusso di partenza

1. Autista apre l’app → inserisce orario partenza, targa, ecc.
2. **Seleziona la propria distinta** dal dropdown (import da file PDF/Excel)
3. L’app **importa il viaggio/percorso** (elenco consegne con coordinate)
4. Mostra mappa + lista fermate
5. Autista può partire

---

## 3. Punto di partenza: dove iniziare?

### Caso A – Consegne in linea
Consegne allineate dal punto **più lontano** al **più vicino** rispetto al magazzino.
- **Soluzione**: partire dal più distante e tornare verso il magazzino.

### Caso B – Consegne a “S”
Consegne a forma di S rispetto al magazzino.
- Non è chiaro quale estremità convenga.
- **Soluzione**: poter **scegliere** il punto di partenza.

### Funzionalità da prevedere
- **Vista per distanza**: elenco fermate ordinate per distanza dal magazzino.
- **Partenza dal più lontano**: ordine automatico dal più distante al più vicino.
- **Selezione manuale**: possibilità di indicare da quale fermata iniziare.
- **Mappa**: testare la visualizzazione con partenza dal punto più lontano.

---

## 4. Dati necessari

| Dato | Dove si trova | Uso |
|------|----------------|-----|
| Distinte disponibili | `Giri lavorati/DDT-[data]/RIEPILOGO/` | Dropdown selezione |
| Codici consegna per distinta | PDF distinta o mappatura | Import percorso |
| Coordinate (lat/lon) | `mappatura_destinazioni.xlsx` colonne P, Q | Mappa e ordinamento |
| Magazzino (punto di riferimento) | Da configurare | Calcolo distanze |

---

## 5. Punti da definire

1. **Formato distinte**: i percorsi vanno letti dai PDF o da un altro file (es. Excel)?
2. **Punto magazzino**: coordinate fisse da impostare o lettura da file?
3. **Storage distinte**: le distinte sono su disco locale; l’app web come le legge? Serve un backend locale (es. Python/Flask) che espone le distinte?
4. **Ordine consegne nel PDF**: corrisponde già all’ordine di visita o va ricalcolato?
5. **Test mappa**: confermare che Leaflet/OpenStreetMap mostri bene partenza dal punto più lontano.

---

## 6. Possibile roadmap

| Fase | Cosa fare |
|------|-----------|
| 1 | Backend locale che legge distinte e mappatura, espone API |
| 2 | Campo "Distinta" nell’app con dropdown (chiamata API) |
| 3 | Import percorso alla selezione distinta |
| 4 | Mappa con fermate in ordine distanza (partenza dal più lontano) |
| 5 | Opzione "Scegli punto di partenza" (clic sulla mappa o sulla lista) |
| 6 | Integrazione orari partenza/arrivo con Google Sheets |

---

*Documento creato per organizzare la discussione. Da aggiornare con le decisioni prese.*
