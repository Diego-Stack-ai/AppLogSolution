# REGOLE E WORKFLOW DELLA PIPELINE LOGISTICA (AGGIORNATO)

Ecco la copia completa e aggiornata delle regole (workflow) seguite dal programma in ordine cronologico.
Tutto il sistema è architettato per funzionare dal "Bat 1" al "Bat 6" (Script Python dal numero 1 al numero 10), garantendo tracciabilità, precisione e ottimizzazione automatica dei percorsi.

---

### STEP 1: Estrazione e Preparazione dei Dati Originali
**Script:** `(1_2_3_4)_estrai_ddt_consegne.py` (Script Master Integrato)
**Regola base:** Questo è l'orchestratore iniziale. Pulisce i file delle sessioni precedenti sporche, si inoltra nelle cartelle dei documenti `FRUTTA` e `LATTE`, scansiona le maxibolle in PDF e le fa a fette: estrae ogni singola pagina cliente e la salva come file autonomo (es. `p1234_data.pdf`).

### STEP 2: Incrocio coi Clienti e Precedenza GPS Autisti (★ AGGIORNATO)
**Script:** `2_crea_punti_consegna.py`
**Regola base:** Incrocia le singole bollette generate dal punto precedente con il foglio centrale `mappatura_destinazioni.xlsx`. 
**Nuova Regola di Sicurezza (GPS):** Quando assegna la posizione geografica a un cliente, controlla PER PRIMA COSA la colonna `COORDINATE_REALI_GPS` in fondo all'Excel. Se trova un salvataggio fatto dall'autista sul campo, usa esclusivamente quello annullando l'indirizzo testuale, garantendo la precisione al millimetro in autostrada. Se non c'è, ripiega sulle coordinate standard di fallback (Lat/Lon). 

### STEP 3: Unificazione Bolle e Rilevamento Anomalie (★ AGGIORNATO)
**Script:** `3_crea_lista_unificata.py`
**Regola base:** Fonde le consegne della Frutta e del Latte che hanno la stessa destinazione in un'unica fermata.
**Nuova Regola (Resi Multipli):** Interroga il registro rientri tramite logica estesa `defaultdict(list)`. Se un cliente ha due o tre diversi DDT storici rimasti "appesi" e mai rientrati, li cataloga tutti insieme facendo scattare allerte multiple combinate sia sulla Mappa che sui fascicoli finali.

### STEP 4: Assegnazione Zone (La Mappa Dispatcher)
**Script:** `4_mappa_zone_google.py`
**Regola base:** Avvia il software di controllo locale (la WebApp gestionale Map). L'utente seleziona i "secchielli" dei punti e li lancia ai vari veicoli in partenza. Chiudendo la pagina salva tutto nel JSON base grezzo.
**Regola di Sicurezza (Storicizzazione):** Appena si assegna un punto a un furgone, il programma incide tempestivamente la scritta temporanea `"in lavorazione"` nell'Excel storico `rientri_ddt`. Se incontra una casella passata in cui c'è già il sigillo `"allegato"`, la ignora per sicurezza impedendo sovrascritture distruttive sui rientri vecchi chiusi!

### STEP 5: Intelligenza Artificiale e Consolidamento Ordine (★ AGGIORNATO)
**Script:** `6_genera_percorsi_veggiano.py` E SUBITO DOPO `8_genera_json_ottimizzato.py` (dentro il *Bat 3*)
**Regola base:** Genera gli HTML stampabili della Mappa a blocchi di Veggiano. Nel farlo affida immediatamente il ricalcolo chilometrico all'Intelligenza Artificiale "Google OR-Tools" per generare la tratta ineguagliabile (con partenza/arrivo dal Deposito). 
**Nuova Regola di Sincronizzazione Pura:** Prima che si chiuda il Bat 3, interviene lo script 8 che incamera questa magnifica sequenza formale creata dal cervellone e la salva indelebilmente in `viaggi_giornalieri_OTTIMIZZATO.json`. In questo modo l'ordine non potrà mai più divergere e farà da Re per tutti i prossimi software. E soprattutto **ignora i punti a vuoto (come DDT_DA_INSERIRE)** estrapolandoli dal giro viaggiabile.

### STEP 6: Interfaccia Mobile Autisti (WhatsApp App)
**Script:** `7_genera_mappe_mobile_autisti.py` (Il *Bat 4*)
**Regola base:** Attinge ciecamente solo al file Re (`OTTIMIZZATO.json`) letto al punto precedente. Compone in pochi secondi la WebApp da cellulare da inoltrare via Whatsapp contenente: ordine di fermata fedelissimo, Link per G-Maps, pulsante "Consegnato" e abilita il tastino segreto **"Geolocalizza"** per far comunicare il telefono con il cloud Firebase di ritorno.

### STEP 7: Generazione Fascicoli Cartacei e Chiusura Contabile
**Script:** `9_genera_distinte_da_viaggi.py` (Il *Bat 5*)
**Regola base:** Attinge anch'esso esclusivamente al file Re unificato. Invece degli HTML sforna i PDF cartacei. 
**Regole Finali:** Cuce e impagina gli originali in due Master PDF. Scrive sulle etichette le specifiche date concatenate del ritiro (es. `[RIENTRO<-['13-04-2026']]`). Poi compie la mossa definitiva: apre il registro Excel, cerca le scritte provvisorie `"in lavorazione"` che aveva lasciato al Punto 4, le vernicia indelebilmente con **"Allegato DDT + la data di oggi"** e chiude l'Excel.

### STEP 8: Rete di Ritorno Punti Precisi (Il Sync di Fine Giornata)
**Script:** `10_sync_coordinate_da_cloud.py` (Il *Bat 6*)
**Regola base:** È il "Ponte Sensoriale". Si autentica in modo sicuro e criptato verso Firebase usando la chiave Service Account. Scarica la posta (cioè rintraccia i nuovi ping GPS perfetti mandati in giornata dai tasti degli autisti di cui al Punto 6). Quando li trova, li incide fisicamente permanentemente in fondo alla colonna T (`COORDINATE_REALI_GPS`) dell'anagrafica clienti del PC in ufficio, preparando il terreno immacolato e perfezionato per il giorno successivo, quando ripartirà il Punto 2!
