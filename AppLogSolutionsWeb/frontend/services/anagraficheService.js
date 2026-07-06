import { initializeApp, getApps, getApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getFirestore, collection, query, getDocs, onSnapshot } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
import { firebaseConfig } from "../firebase-config.js";

const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();
const db = getFirestore(app);

/**
 * Ascolta in realtime una collezione anagrafica generica (es. clienti, articoli, rientri).
 * @param {string} collPath - Il percorso della collezione (es. "clienti/DNR/raccolta clienti").
 * @param {function} callback - Funzione eseguita ogni volta che i dati cambiano.
 * @param {function} onError - Funzione eseguita in caso di errore.
 * @returns {function} unsubscribe - Funzione per fermare l'ascolto.
 */
export function subscribeToAnagrafica(collPath, callback, onError) {
    const q = query(collection(db, collPath));
    return onSnapshot(q, callback, onError);
}
