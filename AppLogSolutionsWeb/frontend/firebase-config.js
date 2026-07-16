// firebase-config.js
// Gestione Multi-Ambiente: Produzione e Sviluppo

const firebaseConfigProd = {
  apiKey: "AIzaSyDLnhP2Q4bz2ubYwcMLiD3-qq4c220eVKw",
  authDomain: "log-solution-60007.firebaseapp.com",
  projectId: "log-solution-60007",
  storageBucket: "log-solution-60007.firebasestorage.app",
  messagingSenderId: "343696844738",
  appId: "1:343696844738:web:b8d4e10c71fb2c67bc7d20"
};

const firebaseConfigDev = {
  apiKey: "AIzaSyCfM1An6ekvcO4Y3a-UooJiEi2g5JkShFQ",
  authDomain: "log-solutions-sviluppo.firebaseapp.com",
  projectId: "log-solutions-sviluppo",
  storageBucket: "log-solutions-sviluppo.firebasestorage.app",
  messagingSenderId: "1097538489312",
  appId: "1:1097538489312:web:03390d3823f80f9c367985"
};

// Riconosciamo l'ambiente dall'URL o se stiamo girando in locale
const isDevEnvironment = window.location.hostname.includes('log-solutions-sviluppo') || 
                         window.location.hostname.includes('--sviluppo') ||
                         window.location.hostname === 'localhost' || 
                         window.location.hostname === '127.0.0.1';

export const firebaseConfig = isDevEnvironment ? firebaseConfigDev : firebaseConfigProd;

if (isDevEnvironment) {
    console.log("[Firebase Config] ATTENZIONE: Connesso all'AMBIENTE DI SVILUPPO (log-solutions-sviluppo)");
} else {
    console.log("[Firebase Config] Connesso alla PRODUZIONE PRINCIPALE (log-solution-60007)");
}
