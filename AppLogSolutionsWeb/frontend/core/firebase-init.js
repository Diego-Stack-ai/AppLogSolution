import { initializeApp, getApps } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { 
    initializeFirestore, 
    getFirestore, 
    persistentLocalCache, 
    persistentSingleTabManager 
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { firebaseConfig } from "../firebase-config.js";

console.log("[DEBUG TRACE] firebase-init.js: inizio inizializzazione app");
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];
console.log("[DEBUG TRACE] firebase-init.js: app inizializzata");

let db;
try {
    console.log("[DEBUG TRACE] firebase-init.js: chiamo initializeFirestore");
    db = initializeFirestore(app, {
        localCache: persistentLocalCache({ tabManager: persistentSingleTabManager({ forceOwnership: true }) })
    });
    console.log("[DEBUG TRACE] firebase-init.js: initializeFirestore completata in try");
    console.log("[Firebase Init] ✅ Offline persistence attiva (IndexedDB, Single-tab).");
} catch (e) {
    console.log("[DEBUG TRACE] firebase-init.js: initializeFirestore fallita, chiamo getFirestore", e);
    db = getFirestore(app);
    console.warn("Offline persistence non abilitata o già inizializzata.");
}

console.log("[DEBUG TRACE] firebase-init.js: inizializzo auth");
const auth = getAuth(app);
console.log("[DEBUG TRACE] firebase-init.js: fine script");

// Inizializzazione dati in memoria (Global State)
window.appData = window.appData || {
    lista_clienti: [],
    lista_autisti: [],
    lista_mezzi: [],
    currentUser: {},
    activeTenant: localStorage.getItem('activeTenant') || 'DNR' // Tenant di default
};

export { app, db, auth };
