// firebase-config.js
// ATTENZIONE: questo file NON deve contenere chiavi reali in produzione.
// Usa questa struttura con valori di esempio; le chiavi vere vanno fornite
// in un file locale non tracciato (es. firebase-config.local.js) oppure tramite
// un sistema di build che sostituisce questi placeholder.

import { initializeApp, getApps } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { 
    initializeFirestore, 
    getFirestore,
    persistentLocalCache, 
    persistentMultipleTabManager 
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
import { getAuth, browserLocalPersistence, setPersistence } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyDLnhP2Q4bz2ubYwcMLiD3-qq4c220eVKw",
  authDomain: "log-solution-60007.firebaseapp.com",
  projectId: "log-solution-60007",
  storageBucket: "log-solution-60007.appspot.com",
  messagingSenderId: "343696844738",
  appId: "1:343696844738:web:b8d4e10c71fb2c67bc7d20"
};

// Singleton initialization
const app = getApps().length > 0 ? getApps()[0] : initializeApp(firebaseConfig);

let db;
try {
    db = initializeFirestore(app, {
        localCache: persistentLocalCache({ tabManager: persistentMultipleTabManager() })
    });
    console.log("[Firebase Init] ✅ Firestore con persistenza attiva.");
} catch (e) {
    db = getFirestore(app);
    console.log("[Firebase Init] ⚠️ Firestore usa istanza esistente.");
}

const auth = getAuth(app);
setPersistence(auth, browserLocalPersistence).catch(console.error);

export { app, db, auth, firebaseConfig };
