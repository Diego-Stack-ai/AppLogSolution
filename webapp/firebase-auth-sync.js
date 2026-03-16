import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getFirestore, collection, getDocs, doc, updateDoc, addDoc, deleteDoc, onSnapshot } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
import { firebaseConfig } from "./firebase-config.js";

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Inizializzazione Listener Realtime
function startRealtimeSync() {
    console.log("Attivazione sincronizzazione realtime...");

    // Listener per Clienti (customers)
    onSnapshot(collection(db, "customers"), (snapshot) => {
        const clienti = [];
        snapshot.forEach((d) => {
            clienti.push({ id: d.id, ...d.data() });
        });
        localStorage.setItem('lista_clienti', JSON.stringify(clienti));
        console.log("Clienti aggiornati realtime:", clienti.length);
        
        // Refresh UI se la funzione esiste nella pagina corrente
        if (typeof window.renderClienti === 'function') window.renderClienti();
    });

    // Listener per Autisti (users)
    onSnapshot(collection(db, "users"), (snapshot) => {
        const autisti = [];
        snapshot.forEach((d) => {
            autisti.push({ id: d.id, ...d.data() });
        });
        localStorage.setItem('lista_autisti', JSON.stringify(autisti));
        console.log("Autisti aggiornati realtime:", autisti.length);
        
        if (typeof window.renderAutisti === 'function') window.renderAutisti();
        if (typeof window.renderAutistiDropdown === 'function') window.renderAutistiDropdown();
    });

    // Listener per Mezzi (mezzi)
    onSnapshot(collection(db, "mezzi"), (snapshot) => {
        const mezzi = [];
        snapshot.forEach((d) => {
            mezzi.push({ id: d.id, ...d.data() });
        });
        localStorage.setItem('lista_mezzi', JSON.stringify(mezzi));
        console.log("Mezzi aggiornati realtime:", mezzi.length);
        
        if (typeof window.renderLista === 'function') window.renderLista();
        if (typeof window.renderMezziInserimento === 'function') window.renderMezziInserimento();
    });
}

// Avvia i listener immediatamente
startRealtimeSync();

// Manteniamo le funzioni per compatibilità retroattiva se richiamate manualmente
window.syncFromFirebase = async function () {
    console.log("Sincronizzazione manuale non più necessaria (realtime attivo)");
}

// Funzione di salvataggio remoto per i clienti
window.updateCustomer = async function(id, data) {
    try {
        const docRef = doc(db, "customers", id);
        const { id: _, ...updateData } = data;
        await updateDoc(docRef, updateData);
        return true;
    } catch (e) {
        console.error("Errore salvataggio Cliente:", e);
        throw e;
    }
}

// Funzione di salvataggio/creazione per gli utenti
window.updateUser = async function(id, data) {
    try {
        const { id: _, ...updateData } = data;
        if (id) {
            const docRef = doc(db, "users", id);
            await updateDoc(docRef, updateData);
        } else {
            await addDoc(collection(db, "users"), updateData);
        }
        return true;
    } catch (e) {
        console.error("Errore salvataggio Utente:", e);
        throw e;
    }
}

// Funzione di salvataggio/creazione per i mezzi
window.updateMezzo = async function(id, data) {
    try {
        const { id: _, ...updateData } = data;
        if (id) {
            const docRef = doc(db, "mezzi", id);
            await updateDoc(docRef, updateData);
        } else {
            await addDoc(collection(db, "mezzi"), updateData);
        }
        return true;
    } catch (e) {
        console.error("Errore salvataggio Mezzo:", e);
        throw e;
    }
}

// Funzione di eliminazione generica
window.deleteFromFirebase = async function(collectionName, id) {
    try {
        const docRef = doc(db, collectionName, id);
        await deleteDoc(docRef);
        return true;
    } catch (e) {
        console.error("Errore eliminazione Firebase:", e);
        throw e;
    }
}

// Attiva ufficialmente Firebase come fonte primaria
window.syncFromCloud = window.syncFromFirebase;

