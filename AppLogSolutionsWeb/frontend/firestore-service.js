import { 
    initializeFirestore,
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
    persistentLocalCache,
    persistentMultipleTabManager
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { initializeApp, getApps } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getStorage, ref as sRef, getDownloadURL } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-storage.js";
import { firebaseConfig } from "./firebase-config.js";

const app = getApps().length > 0 ? getApps()[0] : initializeApp(firebaseConfig);

// ─── PERSISTENZA OFFLINE (IndexedDB) ─────────────────────────────────────────
// Nuova API Firebase 10+: FirestoreSettings.cache con persistentLocalCache.
// Supporta più tab aperti contemporaneamente senza errori (multi-tab manager).
let db;
try {
    db = initializeFirestore(app, {
        cache: persistentLocalCache({ tabManager: persistentMultipleTabManager() })
    });
    console.log("[Firestore] ✅ Offline persistence attiva (IndexedDB, multi-tab).");
} catch (e) {
    // initializeFirestore lancia un errore se Firestore è già stato inizializzato
    // (es. da gps-tracker.js) → usiamo getFirestore() come fallback
    db = getFirestore(app);
    console.log("[Firestore] ✅ Firestore già inizializzato, riuso istanza esistente.");
}

const auth = getAuth(app);

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
    } else {
        const docRef = await addDoc(collection(db, "viaggi"), {
            ...payload,
            createdAt: serverTimestamp()
        });
        console.log(`[Firestore] Nuovo viaggio creato [ID: ${docRef.id}]`);
        // We set tripId so we can return it correctly below
        tripData.id = docRef.id;
    }

    // --- SINCRO AUTOMATICA CON PRESENZE ---
    try {
        if (tripData.data && tripData.autista) {
            const presenzeDocId = `${user.uid}_${tripData.data}`;
            const presenzeRef = doc(db, "presenze", presenzeDocId);
            
            let clientePresenza = tripData.cliente || "";
            if (tripData.viaggio && tripData.viaggio.trim() !== "") {
                clientePresenza += ` - ${tripData.viaggio}`;
            }

            const presenzaPayload = {
                autistaId: user.uid,
                nomeAutista: tripData.autista,
                data: tripData.data,
                cliente: clientePresenza,
                kmPartenza: Number(tripData.kmPartenza) || 0,
                kmArrivo: Number(tripData.kmArrivo) || 0,
                kmDelta: Number(tripData.delta_km) || 0,
                oraInizioM: tripData.mattinaInizio || "",
                oraFineM: tripData.mattinaFine || "",
                oraInizioP: tripData.pomeriggioInizio || "",
                oraFineP: tripData.pomeriggioFine || "",
                oreOrdinarie: Number(tripData.ore_ordinarie) || 0,
                oreStraordinarie: Number(tripData.ore_straordinarie) || 0,
                oreTotali: Number(tripData.ore_totali) || 0,
                note: tripData.nota || "",
                importo: Number(tripData.importo) || 0
            };
            
            await setDoc(presenzeRef, presenzaPayload, { merge: true });
            console.log(`[Firestore] Sincronizzato con presenze [ID: ${presenzeDocId}]`);
        }
    } catch (err) {
        console.error("Errore sincro presenze:", err);
    }

    return tripData.id || tripId;
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

const storage = getStorage(app);

window.firebaseStorage = storage;
window.sRef = sRef;
window.getDownloadURL = getDownloadURL;

// ─── GESTIONE TURNI IN SOSPESO ───────────────────────────────────────────────

/**
 * Controlla se c'è un turno "in corso" per l'autista corrente
 */
export async function checkPendingTrip() {
    const user = auth.currentUser;
    if (!user) return null;

    try {
        const q = query(
            collection(db, "viaggi"),
            where("autistaId", "==", user.uid),
            where("stato", "==", "in corso")
        );
        const snap = await getDocs(q);
        if (!snap.empty) {
            // Prende il primo trovato (dovrebbe essercene uno solo in corso)
            const docSnap = snap.docs[0];
            return { id: docSnap.id, ...docSnap.data() };
        }
    } catch (err) {
        console.error("[Firestore] Errore checkPendingTrip:", err);
    }
    return null;
}

/**
 * Chiude il turno in "anomalia" e segna la riga delle presenze come errata
 */
export async function closeTripWithAnomaly(tripData) {
    const user = auth.currentUser;
    if (!user || !tripData || !tripData.id) return;

    try {
        // 1. Marca il viaggio come anomalia
        const tripRef = doc(db, "viaggi", tripData.id);
        await updateDoc(tripRef, { 
            stato: "anomalia", 
            note: (tripData.nota ? tripData.nota + " | " : "") + "Turno annullato per dimenticanza chiusura",
            updatedAt: serverTimestamp() 
        });

        // 2. Segna le presenze come "hasError"
        if (tripData.data) {
            const presenzeDocId = `${user.uid}_${tripData.data}`;
            const presenzeRef = doc(db, "presenze", presenzeDocId);
            
            await setDoc(presenzeRef, {
                hasError: true,
                note: "Dimenticanza chiusura. Gestione manuale richiesta.",
                autistaId: user.uid,
                nomeAutista: tripData.autista || "",
                data: tripData.data
            }, { merge: true });
        }
        
        console.log(`[Firestore] Viaggio ${tripData.id} chiuso in anomalia.`);
    } catch (err) {
        console.error("[Firestore] Errore closeTripWithAnomaly:", err);
    }
}

export { db, auth, storage, sRef, getDownloadURL };
