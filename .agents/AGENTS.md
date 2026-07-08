# AGENTS.md — Regole Obbligatorie per questo Progetto
# AppLogSolutions Web — G:\Il mio Drive\App

Queste istruzioni sono VINCOLANTI per ogni agente che lavora su questo progetto.
NON devono essere ignorate, aggirate o modificate senza esplicita approvazione dell'utente.

---

## PROCEDURA OBBLIGATORIA: Aggiornamento Versione

Ogni volta che vengono apportate modifiche, sia al frontend che al backend (nuove funzionalita, bugfix, modifiche strutturali), l'agente DEVE SEMPRE far scattare e aggiornare la versione dell'applicazione seguendo QUESTA e SOLO questa procedura.

### File da modificare (ENTRAMBI, sempre insieme):

1. `G:\Il mio Drive\App\AppLogSolutionsWeb\frontend\sw.js` RIGA 1
   const CACHE_NAME = 'log-solution-vX.XX';

2. `G:\Il mio Drive\App\AppLogSolutionsWeb\frontend\script.js` RIGA 7
   const APP_VERSION = "X.XX";

### Regole TASSATIVE:
- NON modificare mai il badge di versione hardcoded in dashboard.html o in qualsiasi altro file HTML. Il badge viene aggiornato automaticamente da script.js tramite document.querySelectorAll('.app-version-badge').
- NON usare grep per finalità di sostituzione/modifica del numero di versione (rischio di rompere SVG o coordinate GPS). L'uso di grep è consentito in sola lettura per le verifiche.
- NON inventare la versione corrente. Controllare SEMPRE script.js riga 7 prima di procedere.
- I query string ?v=X.XX nei tag <link> e <script> di TUTTI i file HTML DEVONO essere aggiornati alla nuova versione. Farlo tramite script Python (NON grep/PowerShell). Questo serve al browser per scaricare i file JS/CSS aggiornati.
- **TASSATIVO — DEPLOY CI/CD:** Dopo la modifica, NON lanciare `firebase deploy --only hosting` manualmente dal terminale locale. L'Hosting viene deployato in automatico tramite GitHub Actions dal branch `main`.

### Sequenza Deploy Versione:
  1. Leggi APP_VERSION attuale da script.js riga 7
  2. Calcola la nuova versione (incremento decimale, es. 2.87 -> 2.88)
  3. Aggiorna sw.js riga 1 con il nuovo CACHE_NAME
  4. Aggiorna script.js riga 7 con il nuovo APP_VERSION
  5. Allinea tutti i ?v= nei file HTML: esegui uno script Python che sostituisce la vecchia versione con la nuova in tutti i *.html del frontend (es. ?v=2.87 -> ?v=2.88). Usare sempre script Python, mai grep/PowerShell.
  6. Verifica con grep che non rimangano riferimenti alla versione precedente nei file HTML.
  7. Fai il `git commit` su `sviluppo` e FERMATI TASSATIVAMENTE per attendere il collaudo umano (vedi sezione Regole sul Deploy).
  8. Solo dopo l'approvazione dell'utente, uniscilo a `main` e fai `git push origin main`. GitHub Actions eseguirà automaticamente il deploy di Hosting in produzione.

---

## Struttura del Progetto

- App Web (Frontend + Cloud Functions): G:\Il mio Drive\App\AppLogSolutionsWeb\
  - Frontend: frontend/
  - Cloud Functions (Python): functions/main.py
- App Locale (script Python standalone): G:\Il mio Drive\AppLogSolutionLocale\dati\PROGRAMMA\
  - **NOTA SINCRO:** L'App Web è al 100% svincolata a livello di codice dall'App Locale. Database (Firestore) e Storage Firebase vengono utilizzati in comune come sorgente di verità, ma senza alcun automatismo in background. Il travaso dati tra i file Excel locali e Firestore avviene solo tramite script manuali dell'operatore.
- Firebase Project principale: log-solution-60007
- Firebase Project muletto (test): log-solution-muletto (TASSATIVO: NON DEVE MAI ESSERE TOCCATO, MODIFICATO O UTILIZZATO PER I DEPLOY SENZA ESPLICITO ORDINE DELL'UTENTE)
- Firestore tenant principale: clienti/DNR/

---

## Regole sul Database (Firestore)

- Le collezioni anagrafiche (raccolta clienti, articoli, orari, rientri) NON vanno mai toccate da operazioni logistiche o di pulizia.
- I dati logistici giornalieri vivono sotto clienti/DNR/reports_logistici/[data_consegna].
- Lo Storage Firebase usa i prefissi: split_ddt/[data]/, REPORTS/[data]/, CONSEGNE/CONSEGNE_[data]/.

---

## Regole sul Deploy (CI/CD Obbligatorio) e ISOLAMENTO AMBIENTI

- **TASSATIVO — ISOLAMENTO TOTALE E DEFINITIVO DEI DUE MONDI (PRODUZIONE vs SVILUPPO):**
  - **PRODUZIONE (`main`):** Qualsiasi operazione di deploy ufficiale (sia Hosting automatico via GitHub che Functions manuali) deve puntare unicamente al progetto `log-solution-60007`.
  - **SVILUPPO (`sviluppo`):** Quando si lavora sul branch `sviluppo`, QUALSIASI operazione di deploy manuale (Hosting o Cloud Functions) DEVE essere indirizzata esclusivamente al progetto di sviluppo (`log-solutions-sviluppo`) aggiungendo il flag `--project log-solutions-sviluppo`. È severamente vietato caricare codice in fase di test sul server di produzione.
- TASSATIVO — DIVIETO SUL MULETTO: Il progetto e ambiente muletto (`log-solution-muletto`) NON DEVE MAI ESSERE TOCCATO o UTILIZZATO.
- **TASSATIVO — STOP PER COLLAUDO UTENTE SULL'APP:** Dopo aver completato la scrittura del codice sul branch `sviluppo` e aver fatto il commit, l'agente DEVE TASSATIVAMENTE FERMARSI e invitare l'operatore umano a testare l'applicazione dal vivo nel proprio ambiente locale/browser. È severamente vietato eseguire il merge su `main` e il push per la CI/CD fino a quando l'utente non rilascerà l'esplicita autorizzazione: "Collaudo superato, procedi al deploy sul main".
- **HOSTING (FRONTEND):** Tassativamente VIETATO fare `firebase deploy --only hosting` verso la produzione manualmente dal terminale locale. Il deploy in produzione avviene IN AUTOMATICO tramite GitHub Actions quando si effettua il `git push origin main`. L'agente deve limitarsi a unire le modifiche su `main` e fare il push. Per l'Hosting dell'ambiente di Sviluppo, è consentito l'uso di `firebase deploy --only hosting --project log-solutions-sviluppo`.
- **FUNCTIONS (BACKEND):** Il deploy delle Cloud Functions si esegue dal terminale locale, ma **TASSATIVAMENTE** specificando sempre il progetto di destinazione: `--project log-solutions-sviluppo` (per i test) o `--project log-solution-60007` (per l'ufficiale, solo dopo approvazione).
- Una sola funzione: `firebase deploy --only functions:nome_funzione --project [NOME_PROGETTO]` (eseguire sempre dalla cartella G:\Il mio Drive\App\AppLogSolutionsWeb).
- NON eseguire mai `firebase deploy` totale senza `--only`.
- **SINCRONIZZAZIONE DATI:** Prima di validare modifiche critiche in sviluppo, usare lo script `sincronizza_dati_freschi.py` per copiare database e cache delle distanze dalla Produzione allo Sviluppo, assicurando test realistici su dati attuali.

---

## Filiera di Controllo Prima di Modificare

Prima di modificare qualsiasi file, l'agente DEVE:
1. Verificare quale file e la sorgente di verita per quella funzionalita.
2. NON usare Set-Content con PowerShell per iniettare codice JS/HTML con backtick o caratteri speciali. Usare SEMPRE script Python scritti con write_to_file ed eseguiti con python.
3. Dopo ogni modifica a elaborazione.html o a qualsiasi pagina con JS, verificare che le stringhe confirm() e i template literal JS siano sintatticamente corretti prima di fare il deploy.

---

## CODICE DI CONDOTTA COMPORTAMENTALE DELL'AGENTE (AI GOVERNANCE)

Ogni agente che opera su questo progetto deve tassativamente rispettare i seguenti principi di lucidità e trasparenza:

1. RIGORE E COERENZA CRITICA: L'agente non deve mai generare spiegazioni accomodanti o inventare pattern di sincronizzazione per compiacere l'utente. Deve analizzare il sistema con occhio critico, basandosi esclusivamente sui fatti riscontrabili nel codice.
2. TRASPARENZA SULLE IPOTESI (AVVISO UMANO): Qualora l'agente sia costretto a teorizzare o immaginare il funzionamento di un componente non ispezionato direttamente, DEVE dichiararlo esplicitamente anteponendo l'etichetta `[⚠️ TEORIA AI / DA VERIFICARE]`.
3. AUTOMONITORAGGIO DERIVA LOGICA: Nelle sessioni di lavoro lunghe o complesse, l'agente deve autovalutare la qualità del proprio contesto. Se rileva il rischio di allucinazioni o di assunzioni non verificate, deve fermare l'esecuzione e richiedere un reset o un allineamento esplicito all'operatore umano.

---

## GOVERNANCE DEL DISASTER RECOVERY E CONTINUITÀ AZIENDALE (CAVEAU DI RINASCITA)

L'infrastruttura aziendale prevede l'istituzione e la manutenzione di un sistema di Disaster Recovery di livello Enterprise situato in `G:\Il mio Drive\CAVEAU_RINASCITA_APP\`, concepito per slegare l'app da guasti cloud o perdite hardware e consentirne la rinascita da zero in 10 minuti netti.

1. **Principio di Recupero Certificato:** Il Caveau non garantisce il recupero dello stato teorico dell'app, ma il recupero dell'ultimo stato operativo verificato e certificato (strettamente associato a timestamp, commit Git, release in vigore e test superati). Solo un pacchetto in possesso di certificazione completa guadagna il titolo di "Punto di Rinascita".
2. **Barriera PRE_BACKUP_CHECK:** Lo script di estrazione DR deve avviare collaudi sintattici (compilazione Python di main.py, check validità JSON cache e controllo file critici). Se il progetto presenta il minimo errore o inconsistenza, il backup si ferma istantaneamente per garantire un caveau incorrotto.
3. **Audit e Segreti:** Il Caveau conserva la memoria evolutiva dell'app in `09_AUDIT_LOG/` (storico di backup, deploy, autori, descrizioni e motivazioni) e archivia le credenziali sensibili esclusivamente in forma protetta/crittografata in `04_SEGRETI/`.
4. **Strategia di Conservazione Fisica e Manutenzione:** Il Caveau Master adotta una triplice architettura ridondata (copia locale G:, copia su supporto fisico esterno USB/HDD, copia remota protetta). Tutte le copie condividono lo stesso checksum SHA256 e manifesto. Ogni mese o trimestre, il sistema esegue la certificazione periodica (verifica hash anti bit-rot, controllo leggibilità e spazio), rendendo il Caveau un organismo mantenuto vivo e pulsante.

---

## VINCOLO OPERATIVO UI E DESIGN SYSTEM

Da questo momento, ogni modifica o creazione UI deve rispettare tassativamente:
- `G:\Il mio Drive\App\AppLogSolutionsWeb\frontend\docs\design-system.md`
- `G:\Il mio Drive\App\AppLogSolutionsWeb\frontend\docs\design-system.json`

**È SEVERAMENTE VIETATO:**
- Creare nuove classi CSS non presenti nel sistema.
- Usare inline styles (es. `<div style="...">`).
- Duplicare componenti UI già esistenti.
- Ignorare lo spacing system o la gerarchia tipografica.

Se una richiesta dell'utente viola il design system, l'agente DEVE fermarsi, NON generare la UI e proporre all'utente un'alternativa coerente con il sistema e le classi esistenti.

- TASSATIVO � DIVIETO ASSOLUTO DI MODIFICA SCRIPT BUMP: � severamente vietato agli agenti modificare, semplificare, tagliare o alterare lo script ump_version.py (che si occupa del calcolo intelligente e progressivo della versione sui file js e html). Lo script deve rimanere cos� com'�. Qualsiasi modifica a questo script richiede una esplicita autorizzazione dell'utente.
