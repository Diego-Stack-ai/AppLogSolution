# PROGETTO CHIUSURA RELEASE E PROMOZIONE PRODUZIONE

## OBIETTIVO DEL DOCUMENTO
Questo documento traccia i requisiti, i test e le procedure per promuovere l'applicazione dal ramo di sviluppo (Cantiere) al ramo di Produzione, assicurando che non vi siano regressioni, dati persi o configurazioni errate.

## AUDIT GLOBALE HARDCODED

In preparazione al rilascio in Produzione, è stato eseguito un audit globale di tutti i valori hardcoded presenti nel progetto `AppLogSolutionsWeb`.
Questo controllo è cruciale per prevenire che dati di Cantiere vengano accidentalmente promossi in Produzione e per identificare il debito tecnico legato all'hardcoding di tenant, path e regole di business.

### Sintesi dell'Audit
* **Perimetro Analizzato:** L'intero repository `AppLogSolutionsWeb`, inclusi script Python, moduli JavaScript, HTML, CSS e configurazioni Firebase (escluse le directory di build e dipendenze esterne come `node_modules` e `.git`).
* **Rischi Principali Rilevati:**
  * Mapping duplicati per tenant come `DNR`, `CATTEL`, `GRAN CHEF`.
  * Riferimenti diretti ai Project ID (`log-solution-60007` vs `log-solutions-cantiere`) all'interno di script e GitHub Actions.
  * Percorsi Storage fissi per l'importazione PDF.
  * Valori di fallback su `DNR` in assenza di tenant esplicito (debito tecnico rilevante).

### Impatto sulla Promozione
Nessun pacchetto può essere promosso in Produzione finché i seguenti hardcoded critici non sono stati risolti o isolati:
1. Gli script di deploy e i file `.firebaserc` non devono mai forzare l'uso del database di Produzione quando eseguiti in locale.
2. I fallback automatici al tenant `DNR` devono essere rimossi o protetti da configurazione.
3. Le configurazioni Firebase nel frontend HTML/JS devono usare variabili d'ambiente (o logica di inizializzazione sicura) invece di chiavi hardcoded se cambiano per ambiente.

Per i dettagli completi, l'inventario esatto e le proposte di mitigazione, fare riferimento al documento separato:
**[REGISTRO_HARDCODED_APPLOGSOLUTIONSWEB.md](./REGISTRO_HARDCODED_APPLOGSOLUTIONSWEB.md)**
