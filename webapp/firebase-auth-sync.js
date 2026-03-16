import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getFirestore, collection, getDocs, doc, updateDoc, addDoc, deleteDoc } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
import { firebaseConfig } from "./firebase-config.js";

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

window.syncFromFirebase = async function () {
    try {
        console.log("Sincronizzazione da Firebase...");

        // Sincronizza Autisti (Users)
        const userSnapshot = await getDocs(collection(db, "users"));
        const autisti = [];
        userSnapshot.forEach((d) => {
            autisti.push({ id: d.id, ...d.data() });
        });
        localStorage.setItem('lista_autisti', JSON.stringify(autisti));

        // Sincronizza Mezzi
        const mezziSnapshot = await getDocs(collection(db, "mezzi"));
        const mezzi = [];
        mezziSnapshot.forEach((d) => {
            mezzi.push({ id: d.id, ...d.data() });
        });
        localStorage.setItem('lista_mezzi', JSON.stringify(mezzi));

        // Sincronizza Clienti (Destinazioni)
        console.log("Sincronizzazione clienti...");
        const custSnapshot = await getDocs(collection(db, "customers"));
        const clienti = [];
        custSnapshot.forEach((d) => {
            clienti.push({ id: d.id, ...d.data() });
        });
        localStorage.setItem('lista_clienti', JSON.stringify(clienti));

        console.log("Dati sincronizzati da Firebase!");

        // Trigger rendering se necessario
        if (typeof renderAutisti === 'function') renderAutisti();
        if (typeof renderLista === 'function') renderLista();

    } catch (e) {
        console.error("Errore sincronizzazione Firebase:", e);
    }
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

