import { initializeApp, getApps } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getFirestore, collection, doc, getDoc, updateDoc, setDoc, deleteDoc, onSnapshot, addDoc } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
import { getAuth, signInWithEmailAndPassword, onAuthStateChanged, signOut, sendPasswordResetEmail, browserLocalPersistence, setPersistence, updatePassword, sendEmailVerification, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
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

// --- FUNZIONI DI SERVIZIO AUTH REMOSSE POICHE' GESTITE CENTRALMENTE ---// --- GESTIONE LOGOUT GLOBALE ---
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
    const isAdminOnlyPage = ['clienti.html', 'impostazioni.html', 'visualizzazione.html', 'mappa_consegne.html', 'dashboard.html', 'link_viaggi.html'].includes(page);
    const isAutistaOnlyPage = ['inserimento.html', 'presenze.html'].includes(page);

    console.log(`Auth Listener: Utente = ${user ? user.uid : 'NULL'}, Pagina Corrente = ${page}`);

    if (user) {
        try {
            // Implementiamo un semplice retry per connessioni mobili instabili
            let userDoc = null;
            let retries = 3;
            while (retries > 0) {
                try {
                    userDoc = await getDoc(doc(db, "dipendenti", user.uid));
                    break;
                } catch (fetchErr) {
                    retries--;
                    if (retries === 0) throw fetchErr;
                    console.warn(`Auth: getDoc fallito, ritento... tentativi rimasti: ${retries}`, fetchErr);
                    await new Promise(r => setTimeout(r, 1000)); // aspetta 1 secondo
                }
            }
            
            if (userDoc && userDoc.exists()) {
                const userData = userDoc.data();

                // --- 2. CONTROLLO CAMBIO PASSWORD FORZATO ---
                if (userData.needsPasswordChange) {
                    console.warn("Auth: Cambio password richiesto.");
                    const newPassword = prompt("Primo Accesso: Inserisci la tua nuova password definitiva (min 6 caratteri):");
                    if (newPassword && newPassword.length >= 6) {
                        try {
                            await updatePassword(user, newPassword);
                            await updateDoc(doc(db, "dipendenti", user.uid), { needsPasswordChange: false });
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
                const nomeUtente = (userData.nome || '').toLowerCase();
                // Diego Boschetto è sempre amministratore a prescindere dal database
                const isDiego = nomeUtente.includes('boschetto diego') || nomeUtente.includes('diego boschetto');
                const isAdmin = role === 'amministratore' || role === 'impiegata' || isDiego;

                window.appData.currentUser = { id: user.uid, email: user.email, ...userData, ruolo: role, isAdmin: isAdmin };
                
                console.log(`Auth: Profilo caricato [${userData.nome}], Ruolo: "${role}", IsAdmin: ${isAdmin}`);


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
                startRealtimeSync(isAdmin);

                // --- LOGICA DI NAVIGAZIONE E PROTEZIONE ---
                
                // 1. Se loggato e su pagina pubblica -> Vai alla home corretta
                if (isPublicPage) {
                    const home = isAdmin ? 'dashboard.html' : 'inserimento.html';
                    console.log(`REDIRECT DEBUG: Pagina pubblica [${page}] -> Home corretta [${home}]`);
                    window.location.replace(home);
                    return;
                }

                // 2. Protezione assoluta: se l'utente NON è amministratore/impiegata, può accedere SOLO a inserimento.html e presenze.html
                if (!isAdmin) {
                    if (page !== 'inserimento.html' && page !== 'presenze.html') {
                        console.error(`REDIRECT DEBUG: Accesso negato a [${page}] per utente non amministratore. Reindirizzamento a inserimento.html.`);
                        window.location.replace('inserimento.html');
                        return;
                    }
                }

            } else {
                console.warn("Auth: Sessione attiva ma profilo Firestore mancante.");
                
                // --- AUTO-FIX DI EMERGENZA ---
                // Se l'utente si è appena loggato con Firebase Auth ma il suo documento in 'dipendenti' non esiste
                // (ad es. database azzerato), chiediamo se vogliamo ricrearlo come amministratore.
                const confirmCreate = confirm("ATTENZIONE: Il tuo utente Firebase esiste, ma il profilo nel database è stato cancellato.\n\nVuoi ricreare automaticamente il tuo profilo come AMMINISTRATORE per poter accedere?");
                
                if (confirmCreate) {
                    try {
                        const newUserData = {
                            email: user.email,
                            nome: user.email.split('@')[0],
                            ruolo: "amministratore",
                            needsPasswordChange: false
                        };
                        await setDoc(doc(db, "dipendenti", user.uid), newUserData);
                        alert("Profilo ricreato con successo! Ora ricaricheremo la pagina per farti entrare.");
                        window.location.reload();
                        return;
                    } catch(e) {
                        alert("Impossibile ricreare il profilo. Controlla le regole Firestore. Dettaglio: " + e.message);
                    }
                }

                alert("ACCESSO NEGATO: Utente autenticato, ma manca il profilo nel Database (Collection 'dipendenti'). L'account potrebbe essere stato disabilitato o cancellato.");
                await window.logoutFirebase();
            }
        } catch (err) {
            console.error("Auth: Errore recupero profilo Firestore:", err);
            let contextMsg = "";
            if (err.message && err.message.includes('permission')) {
                contextMsg = " (Controllo permessi su dipendenti/" + user.uid + ")";
            }
            alert("Errore di connessione al database durante il login: " + err.message + contextMsg);
            await window.logoutFirebase();
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
    const unsubCustomers = onSnapshot(collection(db, "clienti", "DNR", "raccolta clienti"), (snapshot) => {
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
        const unsubUsers = onSnapshot(collection(db, "dipendenti"), (snapshot) => {
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
            const docRef = doc(collection(db, "clienti", "DNR", "raccolta clienti"));
            await setDoc(docRef, updateData);
        } else {
            const docRef = doc(db, "clienti", "DNR", "raccolta clienti", id);
            await setDoc(docRef, updateData, { merge: true }); // setDoc merge previene crash se vuoto
        }
        return true;
    } catch (e) {
        console.error("Errore salvataggio Cliente:", e);
    }
};

// Alias per chiarezza
window.addCustomer = (data) => window.updateCustomer(null, data);

// Funzione di salvataggio/creazione per gli utenti (Solo per Admin)
window.updateUser = async function(id, data) {
    try {
        const { id: _, ...updateData } = data;
        if (id) {
            const docRef = doc(db, "dipendenti", id);
            
            // Se l'email passata è virtuale, non la salviamo nel profilo Firestore
            if (updateData.email && updateData.email.includes('@logsolution.app')) {
                // Impostiamo l'username estratto se non esiste già
                if (!updateData.username) {
                    updateData.username = updateData.email.split('@')[0];
                }
                updateData.email = "";
            }
            
            await updateDoc(docRef, updateData);
        } else {
            console.warn("La creazione di nuovi account richiede l'uso della console Firebase Auth o Cloud Functions.");
        }
        return true;
    } catch (e) {
        console.error("Errore salvataggio Utente:", e);
        throw e;
    }
}

// Funzione per creare un nuovo utente tramite istanza Auth temporanea
window.registerNewUserCloud = async function(email, password, nomeCompleto, ruolo, turno, canElevate) {
    const tempApp = getApps().find(a => a.name === "UserCreationApp") || initializeApp(firebaseConfig, "UserCreationApp");
    const tempAuth = getAuth(tempApp);

    try {
        // Crea l'utente nel database Auth in modo isolato
        const userCredential = await createUserWithEmailAndPassword(tempAuth, email, password);
        const uid = userCredential.user.uid;

        // Estrae lo username pulito (es. "ayoub.berradia")
        const username = email.split('@')[0];

        // Salva il documento profilo in Firestore nella collezione "dipendenti"
        await setDoc(doc(db, "dipendenti", uid), {
            uid: uid,
            nome: nomeCompleto,
            username: username,
            password: password, // Salvata in chiaro ad uso consultativo admin
            email: "",          // Email vuota come richiesto dall'utente
            ruolo: ruolo,
            tipoTurno: turno,
            canElevate: canElevate,
            needsPasswordChange: false, // Non forza il cambio
            createdAt: new Date()
        });

        await signOut(tempAuth);
        return uid;
    } catch (e) {
        console.error("Errore registrazione temporanea:", e);
        throw e;
    }
};

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


