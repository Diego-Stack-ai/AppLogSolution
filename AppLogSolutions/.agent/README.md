# 🗂️ Documentazione Operativa - Gestione DDT e Viaggi

## 1. Panoramica Generale
L’obiettivo del sistema è gestire i DDT dei clienti, creare i giri di consegna ottimizzati e fornire agli autisti una mappa leggera dei punti da raggiungere.

*   **Firebase**: Database operativo (clienti, mezzi, utenti, log viaggi).
*   **Drive**: PDF DDT e mappe leggere per i viaggi.
*   **Python**: Elaborazione DDT, creazione zone, mappe e PDF finali.
*   **App**: Interfaccia per autisti: visualizza punti, registra chilometri/orari/GPS.

## 2. Flusso dei Dati

### 2.1 Inserimento dati operativi
*   Gli autisti inseriscono inizio giro, chilometri, orari e cliente/giro tramite l’app.
*   I dati vengono salvati in realtime su Firebase.

### 2.2 Elaborazione DDT e creazione viaggi (Python)
*   Legge i PDF dei DDT originali da Drive.
*   Suddivide ogni PDF in un PDF singolo per DDT.
*   Legge il file Excel dei DDT non consegnati.
*   Esegue il matching dei DDT con quelli vecchi non consegnati.
*   Assegna i DDT alle zone di consegna.
*   Genera le mappe dei viaggi, con punti colorati per zona (opzione: mappa unica con tutti i viaggi).
*   Permette aggiustamenti manuali tramite menu in linea (spostare clienti tra viaggi).
*   Genera PDF finali dei viaggi e mappe dei punti di consegna.

### 2.3 Distribuzione delle mappe all’app
*   Ogni viaggio ha una pagina HTML leggera con i punti da raggiungere.
*   L’autista seleziona il viaggio → l’app carica la mappa corrispondente.
*   L’app registra chilometri/orari/GPS in Firebase, senza rielaborare mappe o DDT.

## 3. Architettura dei Sistemi
Il sistema è diviso in tre componenti principali:
1.  **Backend Elaborazione (Python)**: Carico pesante, logica di business e generazione documenti.
2.  **Database Realtime (Firebase)**: Stato sincronizzato tra tutti i dispositivi.
3.  **App Mobile (HTML/JS/PWA)**: Interfaccia leggera per l'operatività sul campo.

## 4. Dettagli Operativi

### 4.1 PDF e DDT
*   PDF originali → suddivisi in PDF singoli per DDT.
*   Ogni DDT ha un codice univoco.
*   Python assegna i DDT alle zone e genera i viaggi.
*   I DDT vecchi non consegnati vengono reinseriti nel viaggio corretto.

### 4.2 Mappe
*   Mappe leggere: solo punti di arrivo del viaggio.
*   Visualizzazione nell’app rapida, senza rielaborazioni.
*   Possibile distinguere zone con colori diversi.
*   Opzione futura: spostamento manuale clienti tra viaggi.

### 4.3 LocalStorage
*   Attualmente presente nell’app, ma non serve per dati operativi.
*   I dati reali sono in Firebase e Drive.
*   Può essere usato solo per sessione utente o bozze temporanee.

## 5. Vantaggi dell’architettura
*   Separazione netta tra dati operativi (Firebase) e gestione documenti PDF/Mappe (Python + Drive).
*   L’app rimane leggera e veloce, anche con molti DDT e viaggi.
*   Python gestisce tutto il carico pesante di elaborazione.
*   Facile aggiornare le mappe e i PDF senza influire sull’app.
*   Eliminato rischio di disallineamento tra dispositivi, problemi di cache o LocalStorage.
