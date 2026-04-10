# REGOLE E WORKFLOW DELLA PIPELINE LOGISTICA (SCRIPT DA 1 A 9)
*Aggiornamento: Gestione Rientri Multipli e Automazione Stati - Aprile 2026*

Ecco la copia completa e aggiornata delle regole (workflow) seguite dal programma attraverso l'esecuzione dei vari file Python `.py`.

---

### STEP 1: Estrazione e Preparazione dei Dati Originali
**Script:** `(1_2_3_4)_estrai_ddt_consegne.py` (Script Master Integrato)
**Regola base:** Questo è l'orchestratore. Elimina i file delle sessioni precedenti sporche, dopodiché entra nelle cartelle `FRUTTA` e `LATTE`, scansiona i PDF originali multipagina e divide ogni singola pagina rinominandola in un file autonomo (es. `p1234_data.pdf`).

### STEP 2: Creazione Base Punti Consegna
**Script:** `2_crea_punti_consegna.py`
**Regola base:** Legge i PDF appena suddivisi e incrocia i codici cliente con il file `mappatura_destinazioni.xlsx`. 
**Azione:** Restituisce un'indicazione geografica sommaria creando due file excel per la giornata (uno frutta, uno latte) che contengono l'effettiva presenza in bolla delle merci filtrate.

### STEP 3: Unificazione e Rilevamento Anomalie (★ AGGIORNATO)
**Script:** `3_crea_lista_unificata.py`
**Regola base:** Unisce le consegne di Frutta e Latte dirette a un medesimo indirizzo in un unico punto finale calcolandone le coordinate (salvato in `punti_consegna_unificati.json`).
**NUOVA REGOLA (Rientri Multipli):** Il sistema non si ferma più alla prima data trovata per il rientro. Entra in `.items()` della rubrica rientri e incamera una **lista multipla** (`rientri = defaultdict(list)`). Se uno stesso codice cliente si aspetta indietro 3 DDT arretrati, lo script li accorpa tutti sull'indirizzo e genera allarmi rossi combinati in mappa!

### STEP 4: Assegnazione Zone (★ AGGIORNATO OGGI)
**Script:** `4_mappa_zone_google.py`
**Regola base:** Crea il server web locale (su porta 5000) permettendo di assegnare comodamente sulla mappa interattiva i punti alle vetture e autisti tramite selezione a poligono.
**NUOVA REGOLA (Automazione Excel Sicura):** Quando si salva sulla mappa o si muove un punto, lo script apre i `rientri_ddt.xlsx` e imposta automaticamente lo stato di base provvisorio su `"in lavorazione"` (oppure sposta all'indietro se si annulla). Altrimenti, tramite il blocco di sicurezza odierno, **se una riga del passato storicizzata presenta già la scritta `allegato`, la scavalca rendendola fisicamente intoccabile!**

### STEP 5, 6 e 7: Generazione Moduli di Deposito e Mobile
**Script:** `6_genera_percorsi_veggiano.py` / `7_genera_mappe_mobile_autisti.py`
**Regole base:** Usano l'assegnazione json creata dal dispatcher nello step 4 per i riepiloghi.
* **6_genera (Veggiano):** Costruisce gli HTML stampabili a blocchi per chi deve preparare i bancali nel magazzino.
* **7_genera (WhatsApp App):** Genera la "Mappa Autisti" rapida con i file HTML minimali inviabili via messaggio agli autisti per l'operatività base.

### STEP 8: Ottimizzazione Logistica Cloud e Autisti Avanzati
**Script:** `8_genera_json_ottimizzato.py` e `8_server_mobile_autisti.py` 
**Regola base:** File che alleggeriscono la stringa JSON e avviano l'infrastruttura di connettività verso la Progressive Web App (PWA) e verso Firebase. Permette la pre-carica off-line in assenza di rete dei conducenti e assicura l'operatività dei pulsanti via smartphone.

### STEP 9: Generazione Distinte PDF (★ AGGIORNATO)
**Script:** `9_genera_distinte_da_viaggi.py`
**Regola base:** Genera i fogli PDF estetici finali e cartacei ("Distinte Viaggio"), unendo l'intestazione all'ordine preciso dei clienti serviti con relativo peso, colli, fermate e orari.
**NUOVA REGOLA 1 (Etichette rientri dinamiche):** Nei moduli di consegna stampati, l'autista capirà al volo se ritirare più resi unificati. Invece di "[RIENTRO]", troverà label dinamiche (es. `[RIENTRO<-['13-04-2026', '10-04-2026']]`).
**NUOVA REGOLA 2 (Chiusura Excel Definitiva):** Gira l'ultima validazione ("Finalizzazione Stati"). Tutte le celle provvisorie create in fase 4 con scritto `"in lavorazione"`, ora vengono formalmente cristallizzate, marcate internamente nell'Excel da solo come  `"allegato DDT + {data odierna}"`. Questa ultima firma impedirà automaticamente (vedi regola passo 4 di oggi) qualunque modifica futura sul cliente chiuso.
