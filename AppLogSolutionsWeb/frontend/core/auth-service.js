import { app } from "./firebase-init.js?v=6.039";
import { getAuth, signInWithEmailAndPassword, onAuthStateChanged, signOut, browserLocalPersistence, setPersistence, updatePassword } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

const auth = getAuth(app);

// ABILITAZIONE PERSISTENZA SESSIONE (localStorage)
setPersistence(auth, browserLocalPersistence)
    .catch((error) => console.error("Errore persistenza:", error));

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

let isLoggingOut = false;
window.logoutFirebase = async () => {
    console.log("Auth: Avvio procedura di logout...");
    isLoggingOut = true;
    try {
        window.appData.currentUser = {};
        await signOut(auth);
        console.log("Auth: Logout Firebase completato. Reindirizzamento...");
        window.location.replace('login.html');
    } catch (error) {
        console.error("Auth: Errore durante il logout:", error);
        isLoggingOut = false;
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

    console.log(`Auth Listener: Utente = ${user ? user.uid : 'NULL'}, Pagina Corrente = ${page}`);

    if (user) {
        try {
            // DYNAMIC IMPORT FIRESTORE ONLY IF AUTHENTICATED
            const { getFirestore, doc, getDoc, updateDoc, setDoc } = await import("https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js");
            const db = getFirestore(app);

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
                    await new Promise(r => setTimeout(r, 1000));
                }
            }
            
            if (userDoc && userDoc.exists()) {
                const userData = userDoc.data();

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

                const role = (userData.ruolo || 'autista').toString().toLowerCase().trim();
                const nomeUtente = (userData.nome || '').toLowerCase();
                const isDiego = nomeUtente.includes('boschetto diego') || nomeUtente.includes('diego boschetto');
                const isAdmin = role === 'amministratore' || role === 'impiegata' || isDiego;

                window.appData.currentUser = { id: user.uid, email: user.email, ...userData, ruolo: role, isAdmin: isAdmin };
                
                console.log(`Auth: Profilo caricato [${userData.nome}], Ruolo: "${role}", IsAdmin: ${isAdmin}`);

                let permessiDoc = null;
                try {
                    permessiDoc = await getDoc(doc(db, "config", "permessi_dashboard"));
                } catch(e) {
                    console.warn("Auth: Impossibile scaricare permessi dashboard", e);
                }
                
                const permessiData = permessiDoc && permessiDoc.exists() ? permessiDoc.data() : {};
                window.appData.permessiDashboard = permessiData;

                if (typeof window.onUserProfileLoaded === 'function') {
                    window.onUserProfileLoaded(window.appData.currentUser);
                    setTimeout(() => {
                        if (typeof window.onUserProfileLoaded === 'function') {
                            window.onUserProfileLoaded(window.appData.currentUser);
                        }
                    }, 300);
                }

                // Call startRealtimeSync if loaded
                if (typeof window.startRealtimeSync === 'function') {
                    window.startRealtimeSync(isAdmin);
                }

                if (isPublicPage) {
                    const home = 'dashboard.html';
                    console.log(`REDIRECT DEBUG: Pagina pubblica [${page}] -> Home corretta [${home}]`);
                    window.location.replace(home);
                    return;
                }

                if (page !== 'dashboard.html' && page !== 'login.html') {
                    const pageKey = page.replace('.html', '');
                    window.appData.isReadOnly = false;

                    if (role !== 'amministratore' && !isDiego) {
                        let permLevel = 'none';
                        if (permessiData[pageKey] && typeof permessiData[pageKey][role] !== 'undefined') {
                            const val = permessiData[pageKey][role];
                            if (val === 'write' || val === true) permLevel = 'write';
                            else if (val === 'read') permLevel = 'read';
                            else permLevel = 'none';
                        } else {
                            if (role === 'impiegata') {
                                permLevel = 'write';
                            } else {
                                permLevel = (page === 'inserimento.html' || page === 'presenze.html') ? 'write' : 'none';
                            }
                        }

                        if (permLevel === 'none') {
                            console.error(`REDIRECT DEBUG: Accesso negato a [${page}] per ruolo [${role}]. Reindirizzamento a dashboard.html.`);
                            window.location.replace('dashboard.html');
                            return;
                        }

                        if (permLevel === 'read') {
                            window.appData.isReadOnly = true;
                            console.log(`AUTH DEBUG: Accesso in modalità SOLO LETTURA a [${page}] per ruolo [${role}].`);
                        }
                    }

                    if (window.appData.isReadOnly) {
                        const applyReadOnlyShield = () => {
                            document.querySelectorAll('input:not([id*="search" i]):not([class*="search" i]):not([id*="filter" i]):not([class*="filter" i]), select:not([id*="search" i]):not([class*="search" i]):not([id*="filter" i]):not([class*="filter" i]), textarea').forEach(el => {
                                el.disabled = true;
                                el.style.backgroundColor = '#f8fafc';
                            });
                            document.querySelectorAll('button[type="submit"], .btn-primary, .btn-success, .btn-delete, .btn-add, .delete-btn, .btn-edit, #btnSalva, #updateBtn').forEach(btn => {
                                if (btn.title && btn.title.toLowerCase().includes('mappa')) return;
                                if (!btn.className.toLowerCase().includes('search') && !btn.id.toLowerCase().includes('search') && !btn.className.toLowerCase().includes('tab')) {
                                    btn.style.display = 'none';
                                }
                            });
                            if (typeof window.toggleLockRow === 'function') {
                                document.querySelectorAll('.lock-btn').forEach(btn => btn.style.display = 'none');
                            }
                        };

                        if (document.readyState === 'loading') {
                            document.addEventListener('DOMContentLoaded', applyReadOnlyShield);
                        } else {
                            applyReadOnlyShield();
                        }

                        const observer = new MutationObserver((mutations) => {
                            let shouldReapply = false;
                            for (const mut of mutations) {
                                if (mut.addedNodes.length > 0) {
                                    shouldReapply = true;
                                    break;
                                }
                            }
                            if (shouldReapply) applyReadOnlyShield();
                        });
                        observer.observe(document.body, { childList: true, subtree: true });
                        
                        setTimeout(() => {
                            const banner = document.createElement('div');
                            banner.innerHTML = '<span class="material-icons-round" style="font-size: 16px;">visibility</span> Modalità Solo Lettura. Non hai i permessi per modificare i dati in questa pagina.';
                            banner.style.cssText = 'position:fixed; top:0; left:0; right:0; background:#f59e0b; color:white; text-align:center; padding:6px; font-size:13px; font-weight:bold; z-index:999999; display:flex; justify-content:center; align-items:center; gap:6px; box-shadow:0 2px 10px rgba(0,0,0,0.1);';
                            document.body.appendChild(banner);
                            document.body.style.paddingTop = '32px';
                        }, 500);
                    }
                }

            } else {
                console.warn("Auth: Sessione attiva ma profilo Firestore mancante.");
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

export { auth };
