import { initializeApp, getApps } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { 
    initializeFirestore, 
    getFirestore, 
    persistentLocalCache, 
    persistentMultipleTabManager 
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { firebaseConfig } from "../firebase-config.js";

const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];

let db;
try {
    db = initializeFirestore(app, {
        cache: persistentLocalCache({ tabManager: persistentMultipleTabManager() })
    });
    console.log("[Firebase Init] ✅ Offline persistence attiva (IndexedDB, multi-tab).");
} catch (e) {
    db = getFirestore(app);
    console.log("[Firebase Init] ⚠️ Firestore già inizializzato, riuso istanza esistente.");
}

const auth = getAuth(app);

// Inizializzazione dati in memoria (Global State)
window.appData = window.appData || {
    lista_clienti: [],
    lista_autisti: [],
    lista_mezzi: [],
    currentUser: {},
    activeTenant: localStorage.getItem('activeTenant') || 'DNR' // Tenant di default
};

export { app, db, auth };
