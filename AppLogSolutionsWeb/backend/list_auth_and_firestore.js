const admin = require('firebase-admin');
const serviceAccount = require('./config/log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json');

if (!admin.apps.length) {
    admin.initializeApp({
        credential: admin.credential.cert(serviceAccount)
    });
}

const db = admin.firestore();
const auth = admin.auth();

async function run() {
    console.log("=== COLLEGAMENTO A FIRESTORE (dipendenti) ===");
    const dipRef = db.collection('dipendenti');
    const snap = await dipRef.get();
    const firestoreUsers = [];
    
    snap.forEach(doc => {
        firestoreUsers.push({ id: doc.id, ...doc.data() });
    });
    
    console.log(`Trovati ${firestoreUsers.length} dipendenti in Firestore:`);
    firestoreUsers.forEach(u => {
        console.log(`- Nome: ${u.nome} | Username: ${u.username} | Pwd salvata: ${u.password} | Ruolo: ${u.ruolo} | UID Doc: ${u.uid || doc.id}`);
    });
    
    console.log("\n=== COLLEGAMENTO A FIREBASE AUTHENTICATION ===");
    const authUsers = [];
    let nextPageToken;
    do {
        const listUsersResult = await auth.listUsers(1000, nextPageToken);
        listUsersResult.users.forEach(userRecord => {
            authUsers.push(userRecord.toJSON());
        });
        nextPageToken = listUsersResult.pageToken;
    } while (nextPageToken);
    
    console.log(`Trovati ${authUsers.length} utenti in Firebase Auth:`);
    authUsers.forEach(u => {
        console.log(`- Email: ${u.email} | UID: ${u.uid} | DisplayName: ${u.displayName}`);
    });
}

run().catch(console.error);
