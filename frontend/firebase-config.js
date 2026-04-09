// firebase-config.js
import { firebaseEnv } from "./firebase-config-env.js";

import { initializeApp, getApps } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { 
    initializeFirestore, 
    getFirestore,
    persistentLocalCache, 
    persistentMultipleTabManager 
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
import { getAuth, browserLocalPersistence, setPersistence } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: firebaseEnv.apiKey,
  authDomain: firebaseEnv.authDomain,
  projectId: firebaseEnv.projectId,
  storageBucket: firebaseEnv.storageBucket,
  messagingSenderId: firebaseEnv.messagingSenderId,
  appId: firebaseEnv.appId
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
