import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getFirestore, collection, doc, getDoc, updateDoc, setDoc, deleteDoc, onSnapshot, addDoc } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
import { getAuth, signInWithEmailAndPassword, onAuthStateChanged, signOut, sendPasswordResetEmail, browserLocalPersistence, setPersistence, updatePassword, sendEmailVerification } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { firebaseConfig } from "./firebase-config.js";

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);

// ABILITAZIONE PERSISTENZA SESSIONE (localStorage)
setPersistence(auth, browserLocalPersistence)
    .catch((error) => console.error("Errore persistenza:", error));

// Inizializzazione dati in memoria (Global State)
window.appData = window.appData || {
    lista_clienti: [],
    lista_autisti: [],
    lista_mezzi: [],
    currentUser: {}
};

// --- GESTIONE EMERGENZA (DEBUG) ---
window.forcePasswordResetDebug = async (newPassword) => {
    const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    if (!isLocal) {
        console.warn("Funzione forcePasswordResetDebug disabilitata in produzione.");
        return;
    }
    const user = auth.currentUser;
    if (!user) {
        alert("Nessun utente loggato per il reset.");
        return;
    }
    try {
        await updatePassword(user, newPassword);
        console.log(`[DEBUG] Password aggiornata correttamente per ${user.email}`);
        alert("Password aggiornata con successo via SDK Client.");
    } catch (e) {
        console.error("Errore reset debug:", e);
        alert("Errore reset: " + e.message);
    }
};

// --- FUNZIONI DI SERVIZIO AUTH ---
window.sendVerificationEmail = async () => {
    const user = auth.currentUser;
    if (!user) return alert("Nessun utente loggato.");
    try {
        await sendEmailVerification(user);
        alert("Email di verifica inviata correttamente.");
    } catch (e) {
        alert("Errore invio: " + e.message);
    }
};

// --- GESTIONE AUTENTICAZIONE ---
window.sendResetEmail = async (email) => {
    if (!email) return alert("Email non valida.");
    try {
        await sendPasswordResetEmail(auth, email);
        alert("Email di ripristino password inviata con successo a: " + email);
    } catch (error) {
        console.error("Errore invio email reset:", error);
        alert("Errore nell'invio dell'email: " + error.message);
    }
};

// --- GESTIONE LOGOUT GLOBALE ---
let isLoggingOut = false;
window.logoutFirebase = async () => {
    console.log("Auth: Avvio procedura di logout...");
    isLoggingOut = true;
    try {
        // Puliamo lo stato in memoria prima del logout
        window.appData.currentUser = {};
        
        // Disconnessione da Firebase
        await signOut(auth);
        
        console.log("Auth: Logout Firebase completato. Reindirizzamento...");
        
        // Reindirizzamento alla login pulendo l'URL da eventuali parametri
        window.location.replace('login.html');
        
    } catch (error) {
        console.error("Auth: Errore durante il logout:", error);
        isLoggingOut = false;
        // Fallback: forziamo il reindirizzamento
        window.location.replace('login.html');
    }
};

onAuthStateChanged(auth, async (user) => {
    if (isLoggingOut) {
        console.log("Auth Listener: Logout in corso, salto controlli.");
        return;
    }
    const path = window.location.pathname;
    const page = path.split('/').pop() || 'index.html';
    
    // Classificazione Pagine
    const isPublicPage = page === 'login.html' || page === 'index.html' || page === '';
    const isAdminOnlyPage = ['clienti.html', 'impostazioni.html', 'visualizzazione.html', 'mappa_consegne.html', 'dashboard.html'].includes(page);
    const isAutistaOnlyPage = ['inserimento.html'].includes(page);

    console.log(`Auth Listener: Utente = ${user ? user.uid : 'NULL'}, Pagina Corrente = ${page}`);

    if (user) {
        // --- 1. CONTROLLO EMAIL VERIFICATA ---
        if (!user.emailVerified) {
            console.warn("Auth: Email non verificata.");
            if (!isPublicPage) {
                await signOut(auth);
                window.location.replace('login.html?status=verify_sent');
            }
            return;
        }

        try {
            const userDoc = await getDoc(doc(db, "users", user.uid));
            
            if (userDoc.exists()) {
                const userData = userDoc.data();

                // --- 2. CONTROLLO CAMBIO PASSWORD FORZATO ---
                if (userData.needsPasswordChange) {
                    console.warn("Auth: Cambio password richiesto.");
                    const newPassword = prompt("Primo Accesso: Inserisci la tua nuova password definitiva (min 6 caratteri):");
                    if (newPassword && newPassword.length >= 6) {
                        try {
                            await updatePassword(user, newPassword);
                            await updateDoc(doc(db, "users", user.uid), { needsPasswordChange: false });
                            alert("Password aggiornata con successo! Benvenuto nel sistema.");
                        } catch (e) {
                            alert("Errore durante l'aggiornamento della password: " + e.message + "\nEffettua nuovamente il login.");
                            await signOut(auth);
                            window.location.replace('login.html');
                            return;
                        }
                    } else {
                        alert("Devi cambiare la password per poter accedere al sistema.");
                        await signOut(auth);
                        window.location.replace('login.html');
                        return;
                    }
                }

                // Normalizzazione ruolo (sempre minuscolo e senza spazi)
                const role = (userData.ruolo || 'autista').toString().toLowerCase().trim();
                window.appData.currentUser = { id: user.uid, email: user.email, ...userData, ruolo: role };
                
                console.log(`Auth: Profilo caricato [${userData.nome}], Ruolo: "${role}"`);


                // Hook per aggiornamenti UI nelle pagine
                // Chiamata immediata + retry dopo 300ms per sicurezza su mobile
                if (typeof window.onUserProfileLoaded === 'function') {
                    window.onUserProfileLoaded(window.appData.currentUser);
                    // Retry per dispositivi mobili dove il DOM potrebbe non essere ancora pronto
                    setTimeout(() => {
                        if (typeof window.onUserProfileLoaded === 'function') {
                            window.onUserProfileLoaded(window.appData.currentUser);
                        }
                    }, 300);
                }

                // Avviamo i listener ricaricando i permessi appropriati
                startRealtimeSync(role === 'amministratore' || role === 'impiegata');

                // --- LOGICA DI NAVIGAZIONE E PROTEZIONE ---
                
                // 1. Se loggato e su pagina pubblica -> Vai alla home corretta
                if (isPublicPage) {
                    const home = (role === 'amministratore' || role === 'impiegata') ? 'dashboard.html' : 'inserimento.html';
                    console.log(`REDIRECT DEBUG: Pagina pubblica [${page}] -> Home corretta [${home}]`);
                    window.location.replace(home);
                    return;
                }

                // 2. Protezione pagine Admin (solo admin e impiegata)
                if (isAdminOnlyPage && role === 'autista') {
                    console.error(`REDIRECT DEBUG: Accesso negato a [${page}] per ruolo [autista]. Torno a inserimento.`);
                    window.location.replace('inserimento.html');
                    return;
                }

                // 3. Protezione pagine Autista (solo autista) - NB: Admin può entrare se serve
                if (isAutistaOnlyPage && role === 'impiegata') {
                     // Impiegata magari non deve vedere l'inserimento? 
                     // Per ora la lasciamo entrare se va su inserimento.html, o la rimandiamo a dashboard?
                     // L'utente dice "Amministrativo -> pagine autorizzate specifiche".
                }

            } else {
                console.warn("Auth: Sessione attiva ma profilo Firestore mancante. Logout di sicurezza.");
                await window.logoutFirebase();
            }
        } catch (err) {
            console.error("Auth: Errore recupero profilo Firestore:", err);
        }
    } else {
        // Nessun utente rilevato
        window.appData.currentUser = {};
        if (!isPublicPage) {
            console.log(`REDIRECT DEBUG: Utente non loggato su pagina privata [${page}] -> Redirect a login.html`);
            window.location.replace('login.html');
        }
    }
});

window.loginWithFirebase = async (email, password) => {
    try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        return userCredential.user;
    } catch (error) {
        console.error("Errore Login Firebase:", error.code, error.message);
        throw error;
    }
};

// Inizializzazione Listener Realtime (Condizionali ai permessi)
let activeListeners = [];
function startRealtimeSync(isAdmin) {
    console.log(`Attivazione sincronizzazione realtime (Admin: ${isAdmin})...`);

    // Pulizia listener precedenti se esistenti
    activeListeners.forEach(unsub => unsub());
    activeListeners = [];

    // Listener per Clienti (Punti di Consegna DNR - Progetto Scuole)
    const unsubCustomers = onSnapshot(collection(db, "customers", "DNR", "clienti"), (snapshot) => {
        const clienti = [];
        snapshot.forEach((d) => {
            const data = d.data();
            clienti.push({ 
                id: d.id, 
                ...data,
                nome: data.cliente || data.nome_consegna || data.nome || '',
                codiceFrutta: data.codice_frutta || data.codiceFrutta || '',
                codiceLatte: data.codice_latte || data.codiceLatte || '',
                provincia: data.prov || data.provincia || '',
                lng: data.lon || data.lng || '',
                orarioMin: data.orariomin || data.orarioMin || '',
                orarioMax: data.orariomax || data.orarioMax || ''
            });
        });
        window.appData.lista_clienti = clienti; // Popola correttamente clienti.html
        if (typeof window.renderClienti === 'function') window.renderClienti();
        if (typeof window.renderClientiInserimento === 'function') window.renderClientiInserimento();
    });
    activeListeners.push(unsubCustomers);

    // Listener per Articoli DNR - Progetto Scuole
    const unsubArticoli = onSnapshot(collection(db, "customers", "DNR", "anagrafica_articoli"), (snapshot) => {
        const articoli = [];
        snapshot.forEach((d) => {
            articoli.push({ id: d.id, ...d.data() });
        });
        window.appData.lista_articoli = articoli; // Popola eventuali griglie articoli
        if (typeof window.renderArticoli === 'function') window.renderArticoli();
    });
    activeListeners.push(unsubArticoli);

    // Listener per Autisti/Utenti
    // Se Admin scarica tutti, altrimenti NON scarica nulla (o solo se stesso, già fatto in Auth)
    if (isAdmin) {
        const unsubUsers = onSnapshot(collection(db, "users"), (snapshot) => {
            const autisti = [];
            snapshot.forEach((d) => {
                autisti.push({ id: d.id, ...d.data() });
            });
            window.appData.lista_autisti = autisti;
            if (typeof window.renderAutisti === 'function') window.renderAutisti();
            if (typeof window.renderAutistiDropdown === 'function') window.renderAutistiDropdown();
        });
        activeListeners.push(unsubUsers);
    }

    // Listener per Mezzi (mezzi)
    const unsubMezzi = onSnapshot(collection(db, "mezzi"), (snapshot) => {
        const mezzi = [];
        snapshot.forEach((d) => {
            mezzi.push({ id: d.id, ...d.data() });
        });
        window.appData.lista_mezzi = mezzi;
        if (typeof window.renderLista === 'function') window.renderLista();
        if (typeof window.renderMezziInserimento === 'function') window.renderMezziInserimento();
    });
    activeListeners.push(unsubMezzi);

    // Listener per Progetti (clienti con viaggi associati)
    const unsubProgetti = onSnapshot(collection(db, "progetti"), (snapshot) => {
        const progetti = [];
        snapshot.forEach((d) => {
            progetti.push({ id: d.id, ...d.data(), isProgetto: true });
        });
        window.appData.lista_progetti = progetti;
        if (typeof window.renderProgettiInserimento === 'function') window.renderProgettiInserimento();
        if (typeof window.renderProgettiImpostazioni === 'function') window.renderProgettiImpostazioni();
    });
    activeListeners.push(unsubProgetti);
}

// ─── CRUD PROGETTI ────────────────────────────────────────────────────────────
window.saveProgetto = async function(id, data) {
    try {
        if (id) {
            await updateDoc(doc(db, "progetti", id), data);
        } else {
            await addDoc(collection(db, "progetti"), data);
        }
        return true;
    } catch (e) {
        console.error("Errore salvataggio Progetto:", e);
        throw e;
    }
};

window.deleteProgetto = async function(id) {
    try {
        await deleteDoc(doc(db, "progetti", id));
        return true;
    } catch (e) {
        console.error("Errore eliminazione Progetto:", e);
        throw e;
    }
};

// Funzione di salvataggio/creazione remoto per i clienti (Progetto Scuole DNR)
window.updateCustomer = async function(id, data) {
    try {
        const { id: _, ...updateData } = data;
        let docId = id;
        
        if (!docId) {
            // Se non c'è id creiamo il documento col codice frutta o latte (oppure usiamo addDoc ma setDoc è meglio)
            // Lavoriamo con doc() senza id per generarlo
            const docRef = doc(collection(db, "customers", "DNR", "clienti"));
            await setDoc(docRef, updateData);
        } else {
            const docRef = doc(db, "customers", "DNR", "clienti", id);
            await setDoc(docRef, updateData, { merge: true }); // setDoc merge previene crash se vuoto
        }
        return true;
    } catch (e) {
        console.error("Errore salvataggio Cliente:", e);
        throw e;
    }
}

// Alias per chiarezza
window.addCustomer = (data) => window.updateCustomer(null, data);

// Funzione di salvataggio/creazione per gli utenti (Solo per Admin)
window.updateUser = async function(id, data) {
    try {
        const { id: _, ...updateData } = data;
        if (id) {
            const docRef = doc(db, "users", id);
            await updateDoc(docRef, updateData);
        } else {
            // Nota: La creazione di un nuovo utente Auth richiede Firebase Admin SDK o logic lato server (Cloud Functions)
            // Qui aggiorniamo solo il profilo Firestore se l'UID esiste già
            console.warn("La creazione di nuovi account richiede l'uso della console Firebase Auth o Cloud Functions.");
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
        const targetId = id || updateData.targa;
        if (!targetId) {
            throw new Error("Targa mancante.");
        }
        
        const docRef = doc(db, "mezzi", targetId);
        // Usa setDoc con merge per aggiornare o creare usando la targa come ID
        await setDoc(docRef, updateData, { merge: true });
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


