/**
 * trip-tracker.js — v1.8
 * Sistema di tracciamento viaggio con salvataggio Firestore e logging GPS ogni 3 minuti.
 * Usa la collezione "viaggi" e la sottocollezione "logs".
 * Stabile per mobile: gestisce permessi GPS, errori di rete e riattivazione dopo standby.
 */

import { initializeApp, getApps } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import {
    getFirestore,
    collection, doc,
    setDoc, updateDoc, addDoc,
    serverTimestamp, Timestamp
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { firebaseConfig } from "./firebase-config.js";

// ─── Inizializzazione Firebase (riusa app esistente se già presente) ────────
const app = getApps().length > 0 ? getApps()[0] : initializeApp(firebaseConfig);
const db  = getFirestore(app);
const auth = getAuth(app);

// ─── Stato interno ────────────────────────────────────────────────────────────
let currentTripId   = null;  // ID del documento in "viaggi"
let tripInterval    = null;  // riferimento setInterval (ogni 3 min)
let isTracking      = false; // flag per evitare doppia attivazione

// ─── Banner di stato UI (mostra cosa sta succedendo) ─────────────────────────
function showTrackingBanner(active, message) {
    let banner = document.getElementById('__tracking_banner');
    if (!banner) {
        banner = document.createElement('div');
        banner.id = '__tracking_banner';
        banner.style.cssText = `
            position: fixed; bottom: 80px; left: 16px; right: 16px;
            z-index: 9999; background: #0f766e; color: white;
            padding: 10px 16px; border-radius: 12px;
            font-size: 13px; font-family: inherit;
            display: flex; align-items: center; gap: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            transition: opacity 0.3s ease;
        `;
        document.body.appendChild(banner);
    }
    banner.style.background = active ? '#0f766e' : '#64748b';
    banner.innerHTML = `
        <span class="material-icons-round" style="font-size:18px;">${active ? 'gps_fixed' : 'gps_off'}</span>
        ${message}
    `;
    banner.style.display = 'flex';
    banner.style.opacity = '1';
}

function hideTrackingBanner() {
    const banner = document.getElementById('__tracking_banner');
    if (banner) {
        banner.style.opacity = '0';
        setTimeout(() => { banner.style.display = 'none'; }, 400);
    }
}

// ─── Ottieni posizione GPS (Promise-based, mobile safe) ──────────────────────
function getCurrentPosition() {
    return new Promise((resolve) => {
        if (!navigator.geolocation) {
            console.warn("Tracker: GPS non disponibile su questo browser.");
            resolve(null);
            return;
        }
        navigator.geolocation.getCurrentPosition(
            (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
            (err) => {
                console.warn("Tracker: Errore GPS →", err.message);
                resolve(null); // Fallback: salviamo il log senza coordinate
            },
            { enableHighAccuracy: true, timeout: 8000, maximumAge: 60000 }
        );
    });
}

// ─── Salva un singolo log nella sottocollezione logs ─────────────────────────
async function saveLog(kmCorrente) {
    if (!currentTripId) return;
    try {
        const pos = await getCurrentPosition();
        const logData = {
            timestamp: serverTimestamp(),
            km: kmCorrente !== undefined ? Number(kmCorrente) : null
        };
        if (pos) {
            logData.lat = pos.lat;
            logData.lng = pos.lng;
        }
        const logsRef = collection(db, "viaggi", currentTripId, "logs");
        await addDoc(logsRef, logData);
        console.log(`Tracker: Log salvato [km=${logData.km}, lat=${pos?.lat ?? 'N/A'}, lng=${pos?.lng ?? 'N/A'}]`);
        showTrackingBanner(true, `Tracking attivo — ultimo log ${new Date().toLocaleTimeString('it-IT', {hour:'2-digit', minute:'2-digit'})}`);
    } catch (e) {
        console.error("Tracker: Errore salvataggio log →", e);
        showTrackingBanner(false, "Errore rete — riprovo al prossimo ciclo");
    }
}

// ─── Avvia il tracking ogni 3 minuti ─────────────────────────────────────────
function startTracking() {
    if (isTracking) return;
    isTracking = true;

    // Primo log immediato
    const kmEl = document.getElementById('kmPartenza');
    saveLog(kmEl?.value || null);

    // Poi ogni 3 minuti (180.000 ms)
    tripInterval = setInterval(async () => {
        const kmPartEl = document.getElementById('kmPartenza');
        saveLog(kmPartEl?.value || null);
    }, 180000);

    console.log("Tracker: Tracking avviato (intervallo 3 min).");
}

// ─── FUNZIONE PUBBLICA: Avvia Viaggio ────────────────────────────────────────
window.startTrip = async function(kmPartenza, targa) {
    const user = auth.currentUser;
    if (!user) {
        alert("Errore: nessun utente autenticato.");
        return null;
    }
    if (isTracking) {
        console.warn("Tracker: Viaggio già in corso.");
        return currentTripId;
    }

    try {
        const viaggioRef = doc(collection(db, "viaggi"));
        currentTripId = viaggioRef.id;

        await setDoc(viaggioRef, {
            autistaId:          user.uid,
            stato:              "in corso",
            kmPartenza:         Number(kmPartenza) || 0,
            targa:              targa || "",
            timestampPartenza:  serverTimestamp(),
            kmFine:             null,
            timestampFine:      null
        });

        // Salva l'ID in sessionStorage per recupero dopo refresh mobili
        sessionStorage.setItem('currentTripId', currentTripId);

        console.log(`Tracker: Viaggio avviato [ID: ${currentTripId}]`);
        showTrackingBanner(true, "Viaggio iniziato — tracking GPS attivo");
        startTracking();
        return currentTripId;

    } catch (e) {
        console.error("Tracker: Errore avvio viaggio →", e);
        alert("Errore avvio viaggio: " + e.message);
        return null;
    }
};

// ─── FUNZIONE PUBBLICA: Concludi Viaggio ─────────────────────────────────────
window.endTrip = async function(kmFine) {
    if (!currentTripId) {
        console.warn("Tracker: Nessun viaggio attivo da concludere.");
        return;
    }
    try {
        // Ultimo log prima di chiudere
        await saveLog(kmFine);

        // Aggiorna documento principale
        const viaggioRef = doc(db, "viaggi", currentTripId);
        await updateDoc(viaggioRef, {
            stato:         "concluso",
            kmFine:        Number(kmFine) || 0,
            timestampFine: serverTimestamp()
        });

        // Pulisco stato interno
        clearInterval(tripInterval);
        tripInterval    = null;
        isTracking      = false;
        const closedId  = currentTripId;
        currentTripId   = null;
        sessionStorage.removeItem('currentTripId');

        hideTrackingBanner();
        console.log(`Tracker: Viaggio concluso [ID: ${closedId}]`);
        return closedId;

    } catch (e) {
        console.error("Tracker: Errore conclusione viaggio →", e);
        alert("Errore nel completamento del viaggio: " + e.message);
    }
};

// ─── FUNZIONE PUBBLICA: Recupera viaggio sospeso (after mobile refresh) ──────
window.recoverTrip = function() {
    const savedId = sessionStorage.getItem('currentTripId');
    if (savedId && !isTracking) {
        currentTripId = savedId;
        console.log(`Tracker: Viaggio recuperato dopo refresh [ID: ${currentTripId}]`);
        startTracking();
        showTrackingBanner(true, "Viaggio ripreso dopo interruzione");
        return savedId;
    }
    return null;
};

// ─── FUNZIONE PUBBLICA: Stato corrente del tracker ───────────────────────────
window.getTripStatus = function() {
    return {
        isActive: isTracking,
        tripId:   currentTripId
    };
};

// ─── Auto-recovery: se la pagina si riapre con un viaggio in sessionStorage ──
document.addEventListener('DOMContentLoaded', () => {
    const savedId = sessionStorage.getItem('currentTripId');
    if (savedId) {
        console.log("Tracker: Viaggio pendente trovato in sessione:", savedId);
        // Mostriamo stato UI, ma NON ri-avviamo l'interval automaticamente
        // perché l'utente deve confermare tramite il modale di recupero
        showTrackingBanner(true, "⚠️ Viaggio precedente non concluso — controlla il modale");
    }
});
