const admin = require('firebase-admin');
const serviceAccount = require('./config/log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json');

if (!admin.apps.length) {
    admin.initializeApp({
        credential: admin.credential.cert(serviceAccount)
    });
}

const db = admin.firestore();
const auth = admin.auth();

async function sync() {
    console.log("====================================================");
    console.log("🚀 AVVIO SINCRONIZZAZIONE: FIRESTORE -> FIREBASE AUTH");
    console.log("====================================================\n");

    // 1. Recupero Dipendenti da Firestore
    console.log("📖 Lettura dipendenti da Firestore...");
    const snap = await db.collection('dipendenti').get();
    const firestoreEmployees = [];
    snap.forEach(doc => {
        const data = doc.data();
        firestoreEmployees.push({
            id: doc.id,
            uid: data.uid || doc.id,
            nome: data.nome,
            username: data.username,
            password: data.password,
            ruolo: data.ruolo
        });
    });
    console.log(`✅ Trovati ${firestoreEmployees.length} dipendenti in Firestore.\n`);

    // 2. Recupero Utenti correnti da Firebase Authentication
    console.log("📖 Lettura utenti correnti da Firebase Auth...");
    const authUsers = [];
    let nextPageToken;
    do {
        const listUsersResult = await auth.listUsers(1000, nextPageToken);
        listUsersResult.users.forEach(userRecord => {
            authUsers.push(userRecord.toJSON());
        });
        nextPageToken = listUsersResult.pageToken;
    } while (nextPageToken);
    console.log(`✅ Trovati ${authUsers.length} utenti in Firebase Auth.\n`);

    const authMapByEmail = new Map(authUsers.map(u => [u.email ? u.email.toLowerCase() : '', u]));
    const authMapByUid = new Map(authUsers.map(u => [u.uid, u]));

    // 3. Elaborazione e Sincronizzazione
    console.log("🔄 Allineamento utenti in corso...");
    
    for (const emp of firestoreEmployees) {
        if (!emp.username) {
            console.log(`⚠️ Salto ${emp.nome}: campo 'username' mancante in Firestore.`);
            continue;
        }
        if (!emp.password) {
            console.log(`⚠️ Salto ${emp.nome}: campo 'password' mancante in Firestore.`);
            continue;
        }

        // Generazione email virtuale
        const virtualEmail = `${emp.username.trim().toLowerCase()}@logsolution.app`;
        const expectedUid = emp.uid;

        console.log(`\n👤 Elaboro: ${emp.nome} (${emp.username})`);
        console.log(`   - Email virtuale: ${virtualEmail}`);
        console.log(`   - UID atteso: ${expectedUid}`);

        // Cerca se esiste già l'utente in Auth per UID o per Email
        let existingAuthUser = authMapByUid.get(expectedUid) || authMapByEmail.get(virtualEmail);

        if (existingAuthUser) {
            console.log(`   ✨ Utente Auth esistente trovato (UID: ${existingAuthUser.uid}, Email: ${existingAuthUser.email})`);
            
            // Verifica se i dati corrispondono, altrimenti aggiorna
            const needsUpdate = 
                existingAuthUser.email !== virtualEmail || 
                existingAuthUser.displayName !== emp.nome ||
                !existingAuthUser.emailVerified; // Forza emailVerified a true per evitare blocchi

            // Nota: La password in Auth è cifrata, la aggiorniamo per sicurezza per assicurarci sia allineata a Firestore
            try {
                await auth.updateUser(existingAuthUser.uid, {
                    email: virtualEmail,
                    password: emp.password,
                    displayName: emp.nome,
                    emailVerified: true
                });
                console.log(`   ✅ Dati e Password aggiornati con successo.`);
            } catch (err) {
                console.error(`   ❌ Errore aggiornamento:`, err.message);
            }
        } else {
            console.log(`   🆕 Utente Auth NON esistente. Creazione in corso...`);
            try {
                const newUser = await auth.createUser({
                    uid: expectedUid,
                    email: virtualEmail,
                    password: emp.password,
                    displayName: emp.nome,
                    emailVerified: true
                });
                console.log(`   ✅ Creato con successo in Firebase Auth con UID: ${newUser.uid}`);
            } catch (err) {
                console.error(`   ❌ Errore creazione:`, err.message);
            }
        }
    }

    // 4. Identificazione Utenti Vecchi o Orfani in Firebase Auth
    console.log("\n====================================================");
    console.log("🔍 REPORT UTENTI ORFANI (In Auth ma NON in Firestore)");
    console.log("====================================================");
    
    const activeEmails = new Set(firestoreEmployees.map(emp => `${emp.username.trim().toLowerCase()}@logsolution.app`));
    const activeUids = new Set(firestoreEmployees.map(emp => emp.uid));

    const orphanUsers = authUsers.filter(u => {
        const emailLower = u.email ? u.email.toLowerCase() : '';
        // Un utente è orfano se non corrisponde a nessun UID attivo E a nessuna email attiva
        return !activeUids.has(u.uid) && !activeEmails.has(emailLower);
    });

    if (orphanUsers.length === 0) {
        console.log("🎉 Nessun utente orfano rilevato in Firebase Auth. Ottimo!");
    } else {
        console.log(`Rilevati ${orphanUsers.length} utenti orfani. Di seguito la lista:`);
        orphanUsers.forEach(u => {
            console.log(`- Nome: ${u.displayName || 'N.D.'} | Email: ${u.email} | UID: ${u.uid}`);
        });
        console.log(`\n💡 Suggerimento: Puoi eliminare questi utenti direttamente dalla console Firebase Auth per ripulire il sistema.`);
    }
    
    console.log("\n Sincronizzazione terminata!");
}

sync().catch(console.error);
