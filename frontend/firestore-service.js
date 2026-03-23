import { 
    getFirestore, 
    collection, 
    doc, 
    addDoc, 
    setDoc, 
    updateDoc, 
    getDoc, 
    getDocs, 
    query, 
    where, 
    orderBy, 
    serverTimestamp,
    deleteDoc,
    enableIndexedDbPersistence
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { initializeApp, getApps } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { firebaseConfig } from "./firebase-config.js";

const app = getApps().length > 0 ? getApps()[0] : initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);

// ─── PERSISTENZA OFFLINE (IndexedDB) ─────────────────────────────────────────
// Consente a Firestore di funzionare anche senza connessione.
// Se ci sono più tab aperti, solo il primo attiva la persistenza (multi_tab fallback).
enableIndexedDbPersistence(db)
    .then(() => {
        console.log("[Firestore] ✅ Offline persistence attiva (IndexedDB).");
    })
    .catch((err) => {
        if (err.code === 'failed-precondition') {
            console.warn("[Firestore] ⚠️ Persistenza non attivabile: più tab aperti contemporaneamente.");
        } else if (err.code === 'unimplemented') {
            console.warn("[Firestore] ⚠️ Persistenza non supportata da questo browser.");
        } else {
            console.error("[Firestore] Errore persistence:", err.code);
        }
    });

// ─── SALVA VIAGGIO ────────────────────────────────────────────────────────────
/**
 * Crea o aggiorna un viaggio nella collezione "viaggi".
 * @param {Object} tripData - Dati del viaggio (deve includere 'id' se è un aggiornamento)
 * @returns {string} tripId
 */
export async function saveTrip(tripData) {
    const user = auth.currentUser;
    if (!user) throw new Error("Utente non autenticato");

    console.log("[Firestore] saveTrip chiamato:", tripData);

    const tripId = tripData.id || tripData.tripId || null;
    
    // Pulisce i campi id/tripId dal payload per non duplicarli nel documento
    const { id: _id, tripId: _tripId, ...cleanData } = tripData;

    const payload = {
        ...cleanData,
        autistaId: user.uid,
        updatedAt: serverTimestamp()
    };

    if (tripId) {
        const tripRef = doc(db, "viaggi", tripId);
        await updateDoc(tripRef, payload);
        console.log(`[Firestore] Viaggio aggiornato [ID: ${tripId}]`);
        return tripId;
    } else {
        const docRef = await addDoc(collection(db, "viaggi"), {
            ...payload,
            createdAt: serverTimestamp()
        });
        console.log(`[Firestore] Nuovo viaggio creato [ID: ${docRef.id}]`);
        return docRef.id;
    }
}

// ─── LISTA VIAGGI ─────────────────────────────────────────────────────────────
/**
 * Recupera tutti i viaggi, opzionalmente filtrati per autista.
 * @param {string} autistaNome - Nome autista o 'tutti'
 */
export async function getAllTrips(autistaNome = 'tutti') {
    console.log(`[Firestore] getAllTrips: filtro autista = "${autistaNome}"`);

    let q;
    if (autistaNome !== 'tutti') {
        q = query(
            collection(db, "viaggi"),
            where("autista", "==", autistaNome),
            orderBy("data", "desc")
        );
    } else {
        q = query(collection(db, "viaggi"), orderBy("data", "desc"));
    }

    const snapshot = await getDocs(q);
    const trips = snapshot.docs.map(d => ({ id: d.id, ...d.data() }));
    console.log(`[Firestore] ${trips.length} viaggi recuperati.`);
    return trips;
}

// ─── LOG GPS ──────────────────────────────────────────────────────────────────
/**
 * Recupera i log GPS di un viaggio, filtrati e ordinati.
 * Scarta log senza coordinate valide o con accuratezza scarsa.
 * @param {string} tripId
 */
export async function getTripLogs(tripId) {
    if (!tripId) return [];

    const logsRef = collection(db, "viaggi", tripId, "logs");
    const q = query(logsRef, orderBy("timestamp", "asc"));
    const snapshot = await getDocs(q);

    const allLogs = snapshot.docs.map(d => d.data());
    const validLogs = allLogs.filter(log =>
        log.lat && log.lng &&
        !isNaN(log.lat) && !isNaN(log.lng) &&
        (!log.accuracy || log.accuracy <= 50)
    );

    console.log(`[Firestore] getTripLogs: ${allLogs.length} totali, ${validLogs.length} validi.`);
    return validLogs;
}

// ─── ELIMINA VIAGGIO ──────────────────────────────────────────────────────────
/**
 * Elimina un viaggio e tutti i suoi log GPS.
 * @param {string} tripId
 */
export async function deleteTrip(tripId) {
    console.log(`[Firestore] Eliminazione viaggio [ID: ${tripId}]...`);

    const logsRef = collection(db, "viaggi", tripId, "logs");
    const snapshot = await getDocs(logsRef);
    const deletePromises = snapshot.docs.map(d => deleteDoc(d.ref));

    await Promise.all(deletePromises);
    await deleteDoc(doc(db, "viaggi", tripId));

    console.log(`[Firestore] Viaggio ${tripId} eliminato con ${snapshot.docs.length} log.`);
}

export { db, auth };
