const admin = require('firebase-admin');
const path = require('path');

// Percorso della chiave del service account (recuperato dalla configurazione esistente)
const serviceAccount = require('./config/log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json');

if (!admin.apps.length) {
    admin.initializeApp({
        credential: admin.credential.cert(serviceAccount)
    });
}

const db = admin.firestore();
const auth = admin.auth();

/**
 * Funzione per creare un nuovo utente nel sistema Log-Solution.
 * @param {string} email - Email dell'utente.
 * @param {string} tempPassword - Password temporanea (min 6 caratteri).
 * @param {string} nomeCompleto - Nome e Cognome dell'autista.
 * @param {string} ruolo - Ruolo (autista, impiegata, amministratore). Default: autista.
 */
async function registerUser(email, tempPassword, nomeCompleto, ruolo = 'autista') {
    console.log(`--- Inizio creazione utente: ${nomeCompleto} (${email}) ---`);
    try {
        // 1. Creazione Account in Firebase Authentication
        const userRecord = await auth.createUser({
            email: email,
            password: tempPassword,
            displayName: nomeCompleto,
            emailVerified: false // Obbligatorio verificare via email
        });

        const uid = userRecord.uid;
        console.log(`[AUTH] Utente creato correttamente. UID: ${uid}`);

        // 2. Creazione Profilo in Firestore (Collezione "users")
        // Seguiamo lo standard ID = UID per normalizzazione
        await db.collection('users').document(uid).set({
            uid: uid,
            nome: nomeCompleto,
            email: email,
            ruolo: ruolo,
            tipoTurno: 'giornata', // Default
            needsPasswordChange: true, // Flag per forzare il cambio al primo login
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });
        console.log(`[FIRESTORE] Profilo creato per ${nomeCompleto}.`);

        // 3. Generazione link di verifica (opzionale se si vuole inviare manualmente, 
        // altrimenti Firebase lo farà al primo tentativo di login se implementato nel frontend)
        const actionCodeSettings = {
            url: 'https://log-solution-60007.web.app/login.html?status=verified',
            handleCodeInApp: false
        };
        const verificationLink = await auth.generateEmailVerificationLink(email, actionCodeSettings);
        
        console.log(`[EMAIL] Link di verifica generato: ${verificationLink}`);
        console.log(`\n✅ UTENTE PRONTO.`);
        console.log(`Comunica all'utente la password temporanea: ${tempPassword}`);
        console.log(`L'utente dovrà cliccare sul link ricevuto via email per attivare l'account.`);

    } catch (error) {
        console.error(`[ERRORE] Impossibile creare l'utente:`, error.message);
    }
}

// Esempio di utilizzo (decommentare per test):
// registerUser('test@logsolution.app', 'LogPass2026!', 'Utente Test');

module.exports = { registerUser };
