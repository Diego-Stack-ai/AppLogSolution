import { initializeApp, getApps, getApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getFirestore, collection, getDocs, doc, getDoc, setDoc, query, where } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
import { firebaseConfig } from "../firebase-config.js";

const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();
const db = getFirestore(app);

/**
 * Recupera l'elenco degli autisti dal database.
 * @returns {Promise<Array>} Array di dipendenti (solo autisti attivi).
 */
export async function getAutistiAttivi() {
    const dipendentiSnap = await getDocs(collection(db, "dipendenti"));
    let dipendenti = [];
    
    dipendentiSnap.forEach(d => {
        const data = d.data();
        const ruolo = (data.ruolo || "").toLowerCase().trim();
        const isStaff = ruolo === 'amministratore' || ruolo === 'impiegata';
        
        const stato = (data.stato || data.Stato || "").toLowerCase();
        let isFired = stato.includes('licenziat') || stato.includes('inattiv');
        
        if (!isFired) {
            for (const key in data) {
                if (key.toLowerCase().includes('licenziam') || key.toLowerCase().includes('dimission')) {
                    if (data[key]) {
                        isFired = true;
                        break;
                    }
                }
            }
        }

        // Escludiamo lo staff e i licenziati
        if (data.attivo !== false && !isStaff && !isFired) {
            dipendenti.push({ id: d.id, ...data });
        }
    });
    
    dipendenti.sort((a, b) => {
        const nomeA = ((a.nome || '') + ' ' + (a.cognome || '')).trim();
        const nomeB = ((b.nome || '') + ' ' + (b.cognome || '')).trim();
        return nomeA.localeCompare(nomeB);
    });
    
    return dipendenti;
}

/**
 * Recupera lo storico presenze per calcolare le affinità, a partire da una certa data.
 * @param {string} limiteDataIso - Data limite da cui partire (es. '2026-06-01').
 * @returns {Promise<Array>}
 */
export async function getStoricoPresenze(limiteDataIso) {
    // Al momento l'app legge tutte le presenze e le filtra lato client. 
    // In futuro potremo usare una query() con where() se necessario.
    const presenzeSnap = await getDocs(collection(db, "presenze"));
    let storico = [];
    presenzeSnap.forEach(p => {
        const pd = p.data();
        if (pd.data && pd.data >= limiteDataIso) {
            storico.push(pd);
        }
    });
    return storico;
}
