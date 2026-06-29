# 📖 MANUALE DI GESTIONE UMANA — Disaster Recovery Autonomo \& Rinascita

Questo manuale è stato scritto appositamente in **linguaggio umano, chiaro e privo di acronimi oscuri**. È concepito per te, per un tuo futuro collaboratore o per un successore aziendale che debba assumere il controllo totale del sistema di Disaster Recovery (DR) senza dover possedere conoscenze di programmazione avanzate.

\---

## 🧭 Capitolo 1: Come Capire il Sistema in 60 Secondi

Questo sistema non è un semplice "hard disk di riserva" dove i file vengono copiati e dimenticati, ma un **robot autonomo e vivente**.
Il suo compito è assicurarsi che tu possa ricostruire la tua azienda da zero in qualsiasi momento.

### 🤖 La Regola del "Backup Vivente"

Ogni notte (o quando decidi tu), il motore esegue una filiera implacabile in 6 tempi:

```
🔁 1. Cattura ──> 2. Verifica ──> 3. Valida ──> 4. Pubblica ──> 5. Si Auto-Testa ──> 6. Si Auto-Certifica
```

**La Garanzia Anti-Corruzione**: Se durante questo percorso un singolo file risulta troncato, un calcolo di distanza corrotto o un certificato errato, **il sistema cancella e disintegra immediatamente il backup fallito**. Questo garantisce che nel tuo Caveau entrino solo ed esclusivamente salvataggi perfetti al 100%.

\---

## 🚀 Capitolo 2: Istruzioni Pratiche per l'Accensione

Il sistema risiede interamente all'interno della cartella `G:\\Il mio Drive\\App\\AppLogSolutionsWeb\\dr\_system\\`.
Attualmente è in stato **Dormiente (PAUSED\_DORMIENTE)** per non appesantire il tuo PC. Quando vorrai risvegliarlo, avrai due strade:

### ⚡ Metodo 1: L'Attivazione Immediata (Manuale dal tuo PC)

Se vuoi creare un salvataggio supremo all'istante (ad esempio prima di una vacanza o di un grande aggiornamento):

1. Apri il terminale del PC all'interno della cartella del progetto web (`AppLogSolutionsWeb`).
2. Digita questo singolo comando:

```bash
   python dr\_system/dr\_orchestrator.py
   ```

3. Guarda lo schermo: vedrai il sistema eseguire le fasi di cattura, calcolare i codici crittografici SHA256, lanciare il test di ripristino e rilasciarti un certificato verde di successo.

### 🌙 Metodo 2: L'Automazione Notturna (Google Cloud Scheduler)

Per fare in modo che il backup avvenga da solo ogni notte alle ore 2:00:

1. Accedi alla console di Google Cloud Platform (sezione *Cloud Scheduler*).
2. Carica le impostazioni presenti nel file `dr\_system/scheduler\_config/cloud\_scheduler.json`.
3. Attiva il timer (`0 2 \* \* \*`). Da quel momento, il sistema farà tutto da solo ogni notte mentre dormi.

\---

## 📊 Capitolo 3: Come Leggere i Log e i Referti

Non dovrai mai indovinare se un backup è andato a buon fine. Il sistema scrive un referto esplicito all'interno della cartella `dr\_system/logs/`.
I file più importanti da consultare sono due:

### 1\. 📄 `backup\_report.json` (La Pagella Finale)

Questo file è il certificato ufficiale di rinascita. Aprilo con un Blocco Note per leggere il risultato:

* **`status: "VALID"`**: Significa che tutti i file sono perfetti, pesanti il numero esatto di byte e crittograficamente inattaccabili.
* **`restore\_test: "PASS"`**: Significa che il sistema ha provato a caricare il backup in una sandbox di test e il database ha risposto correttamente.
*(Se leggi `INVALID` o `FAIL`, il sistema avrà già eliminato il file guasto per proteggerti).*

### 2\. 📄 `env\_snapshot.json` (La Fotografia del Motore)

Registra le esatte versioni di Python, Node.js e librerie in uso al momento del backup. Serve per impedire che futuri aggiornamenti esterni (tra 3 o 5 anni) rompano la compatibilità.

\---

## 🚨 Capitolo 4: Guida alla Risoluzione Problemi (Troubleshooting)

Il sistema possiede un motore di autotutela (*Fail-Safe*). Ecco cosa fa e come comportarsi in caso di guasto:

* **❌ Errore di esportazione Firestore (Connessione Assente)**: Lo script tenta automaticamente il recupero per 3 volte a distanza di 5 secondi. Se continua a fallire, annulla l'operazione e ti invia un avviso nel log.
* **❌ Mismatch Crittografico (File Alterato o Bit-rot)**: Se un virus o un calore anomalo sul disco altera un singolo numero in un file delle distanze, il calcolo SHA256 non coinciderà più. Lo script elimina immediatamente il file corrotto e stampa in rosso l'errore in `dr\_orchestrator.log`.
* **❌ Test di Ripristino Fallito**: Se il progetto mock di prova (`test-dr`) rifiuta il caricamento, il backup viene considerato "Non Rinascibile" e invalidato.

\---

## 🌅 Capitolo 5: LA PROCEDURA SUPREMA DI RINASCITA (Tabula Rasa)

Cosa fare se il tuo PC è andato distrutto e l'account Firebase originale è stato cancellato per sempre:

### 🛠️ Passo 1: Configurazione del PC Vergine

1. Accendi un computer nuovo e installa Python 3, Node.js e Git.
2. Collega la chiavetta USB o accedi al Google Drive dove hai conservato il pacchetto di Disaster Recovery.

### 🌐 Passo 2: Creazione del Nuovo Progetto Cloud

1. Apri il browser su `console.firebase.google.com` e crea un nuovo progetto (es. `log-solution-rinato`).
2. Attiva il database Firestore in modalità produzione e il bucket di Cloud Storage.

### 🗂️ Passo 3: Iniezione dei Dati dal Backup

1. **Ripristino Database**: Apri il terminale e inietta l'export Firestore salvato sul nuovo progetto:

```bash
   gcloud firestore import gs://DR-CAVEAU/YYYY-MM-DD/firestore\_export
   ```

2. **Ripristino Storage**: Ricarica il tesoro chilometrico (le cartelle `caches`, `split\_ddt`, `REPORTS`) nel nuovo bucket:

```bash
   gsutil -m rsync -r gs://DR-CAVEAU/YYYY-MM-DD/storage\_sync gs://log-solution-rinato.appspot.com
   ```

### 🏎️ Passo 4: Avvio dei Motori

1. Installa gli strumenti di deploy (`npm install -g firebase-tools`).
2. Sostituisci il nome del progetto nel file `.firebaserc` (da `log-solution-60007` a `log-solution-rinato`).
3. Effettua il deploy finale in 2 comandi:

```bash
   firebase deploy --only functions
   firebase deploy --only hosting
   ```

**Fine della procedura**: In meno di 10 minuti, l'azienda torna operativa al 100%, identica all'esatto millesimo di secondo dell'ultimo stato stabile certificato!

\---

*Manuale Gestione Umana DR — Ultimo aggiornamento: Giugno 2026 (Versione 3.00)*

