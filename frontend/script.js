/**
 * script.js - v1.33
 * Modulo principale per la gestione della UI, validazioni e wizard.
 * Logica di persistenza spostata su firestore-service.js
 */

const APP_VERSION = "1.50";

// Esposta su window per lettura globale (es. da qualsiasi pagina o modulo)
window.APP_VERSION = APP_VERSION;
console.log(`[App] Log Solution PWA â€” versione ${APP_VERSION}`);


// --- STATO GLOBALE ---
window.appData = window.appData || {
    lista_clienti: [],
    lista_autisti: [],
    lista_mezzi: [],
    currentUser: {}
};

// --- HELPERS TEMPO ---
window.getTimeValue = (id) => {
    const h = document.getElementById(id + 'HH')?.value;
    const m = document.getElementById(id + 'MM')?.value;
    if (!h || !m) return "";
    return `${h}:${m}`;
};

window.setTimeValue = (id, val) => {
    if (!val || !val.includes(':')) return;
    const [h, m] = val.split(':');
    const hEl = document.getElementById(id + 'HH');
    const mEl = document.getElementById(id + 'MM');
    if (hEl) hEl.value = h;
    if (mEl) mEl.value = m;
};

// Funzione mostrare/nascondere password
window.togglePasswordVisibility = function() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');
    if (!passwordInput || !toggleIcon) return;
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.textContent = 'visibility_off';
    } else {
        passwordInput.type = 'password';
        toggleIcon.textContent = 'visibility';
    }
};

// --- NAVIGAZIONE ---
window.navigateWithState = (page) => window.location.href = page;

// --- GESTIONE TURNI (WIZARD) ---
let currentStep = 1;
const totalSteps = 2;

window.nextStep = (step) => {
    currentStep = step;
    updateStepUI();
    saveDraft();
};

window.prevStep = (step) => {
    currentStep = step;
    updateStepUI();
};

function updateStepUI() {
    const containers = document.querySelectorAll('.step-container');
    if (containers.length === 0) return;

    containers.forEach(c => c.classList.remove('active'));
    document.getElementById(`step-${currentStep}`)?.classList.add('active');

    for (let i = 1; i <= totalSteps; i++) {
        const dot = document.getElementById(`dot-${i}`);
        if (!dot) continue;
        if (i < currentStep) { dot.classList.add('completed'); dot.innerHTML = 'âœ“'; }
        else if (i === currentStep) { dot.classList.add('active'); dot.classList.remove('completed'); dot.innerHTML = i; }
        else { dot.classList.remove('active', 'completed'); dot.innerHTML = i; }
    }
    
    // Disabilita campi step precedenti
    if (currentStep > 1) {
        document.querySelectorAll('#step-1 input, #step-1 select').forEach(el => {
            el.classList.add('readonly-field');
            el.disabled = true;
        });
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
    if (typeof calcolaTutto === 'function') calcolaTutto();
}

// --- CALCOLI KM E ORE ---
function calcolaTutto() {
    const kmP = parseFloat(document.getElementById('kmPartenza')?.value) || 0;
    const kmA = parseFloat(document.getElementById('kmArrivo')?.value) || 0;
    const deltaEl = document.getElementById('deltaKm');
    if (deltaEl) deltaEl.value = (kmA - kmP) > 0 ? (kmA - kmP) : '-';

    // Calcolo ore: da Ora Inizio a Ora Fine (flusso semplificato a 2 step)
    const oraInizio = window.getTimeValue('oraInizio');
    const oraFine = window.getTimeValue('oraFine');

    let totalM = 0;
    if (oraInizio && oraFine) totalM = diffMin(oraInizio, oraFine);

    if (totalM > 0) {
        const ordM = Math.min(totalM, 480);
        const straM = Math.max(0, totalM - 480);
        document.getElementById('totaleOre').value = formatHHMM(totalM);
        document.getElementById('oreOrdinarie').value = formatHHMM(ordM);
        document.getElementById('oreStraordinario').value = formatHHMM(straM);
    }
}

function diffMin(s, e) {
    const [h1, m1] = s.split(':').map(Number);
    const [h2, m2] = e.split(':').map(Number);
    return Math.max(0, (h2 * 60 + m2) - (h1 * 60 + m1));
}

function formatHHMM(min) {
    const h = Math.floor(min / 60);
    const m = min % 60;
    return `${h}:${m.toString().padStart(2, '0')}`;
}

// --- BOZZE ---
function saveDraft() {
    const draft = { step: currentStep, data: {}, timestamp: Date.now() };
    const ids = ['data', 'automezzo', 'clienteSelect', 'viaggioSelect', 'kmPartenza', 'kmArrivo', 'importo', 'litri', 'nota'];
    ids.forEach(id => { const el = document.getElementById(id); if (el) draft.data[id] = el.value; });
    ['oraInizio', 'oraFine'].forEach(id => { draft.data[id] = window.getTimeValue(id); });
    sessionStorage.setItem('currentDraft', JSON.stringify(draft));
}

window.resumeDraft = () => {
    const saved = sessionStorage.getItem('currentDraft');
    if (!saved) return;
    const draft = JSON.parse(saved);
    Object.keys(draft.data).forEach(id => {
        if (id.includes('Inizio') || id.includes('Fine')) window.setTimeValue(id, draft.data[id]);
        else { const el = document.getElementById(id); if (el) el.value = draft.data[id]; }
    });
    if (document.getElementById('clienteSelect')?.value) window.updateViaggi();
    
    // Ripristina Tracking se necessario
    if (window.recoverGPSTracking) window.recoverGPSTracking();

    currentStep = draft.step;
    updateStepUI();
    document.getElementById('recoveryTripModal')?.classList.remove('active');
};

window.discardDraft = () => {
    sessionStorage.clear();
    window.location.reload();
};

// --- MENÃ™ DINAMICI ---
window.renderMezziInserimento = function() {
    const select = document.getElementById('automezzo');
    if (!select) return;
    const mezzi = window.appData.lista_mezzi || [];
    const currentVal = select.value;
    
    select.innerHTML = '<option value="">Seleziona targa...</option>';
    mezzi.sort((a,b) => a.targa.localeCompare(b.targa)).forEach(m => {
        const opt = document.createElement('option');
        opt.value = m.targa;
        opt.textContent = m.modello ? `${m.targa} (${m.modello})` : m.targa;
        select.appendChild(opt);
    });
    if (currentVal) select.value = currentVal;
};

window.renderClientiInserimento = function() {
    const select = document.getElementById('clienteSelect');
    if (!select) return;

    // 1. Usa lista_progetti da Firestore se disponibile
    const progetti = window.appData.lista_progetti || [];
    let nomi = progetti.map(p => p.nome).filter(Boolean);

    // 2. Fallback hardcoded se Firestore Ã¨ vuoto
    if (nomi.length === 0) {
        nomi = ["PROGETTO SCUOLE", "CATTEL", "GRAN CHEF", "BAUER"];
    }

    const currentVal = select.value;
    select.innerHTML = '<option value="">Seleziona cliente</option>';
    nomi.sort().forEach(nome => {
        const opt = document.createElement('option');
        opt.value = nome;
        opt.textContent = nome.toUpperCase();
        select.appendChild(opt);
    });
    if (currentVal) select.value = currentVal;
};

// Alias usato dal listener realtime
window.renderProgettiInserimento = window.renderClientiInserimento;

window.updateViaggi = function() {
    const clienteNome = document.getElementById("clienteSelect")?.value || "";
    const viaggioSelect = document.getElementById("viaggioSelect");
    if (!viaggioSelect) return;

    viaggioSelect.innerHTML = '<option value="">Seleziona viaggio</option>';
    viaggioSelect.disabled = true;

    // 1. Cerca il progetto su Firestore (lista_progetti)
    const progetto = (window.appData.lista_progetti || []).find(
        p => (p.nome || '').toUpperCase() === clienteNome.toUpperCase()
    );
    let options = progetto ? (progetto.viaggi || []) : [];

    // 2. Fallback hardcoded se non trovato su Firestore
    if (options.length === 0) {
        const viaggiMap = {
            "PROGETTO SCUOLE": ["VIAGGIO 01", "VIAGGIO 02", "VIAGGIO 03", "VIAGGIO 04", "VIAGGIO 05", "VIAGGIO 06", "VIAGGIO 07", "VIAGGIO 08", "VIAGGIO 09", "VIAGGIO 10"],
            "CATTEL": ["BS * BRESCIA", "FBS * FUORI BRESCIA"],
            "GRAN CHEF": ["BL 1 * BELLUNO", "BS * BRESCIA"],
            "BAUER": ["VI * VICENZA", "TV * TREVISO"]
        };
        options = viaggiMap[clienteNome.toUpperCase()] || [];
    }

    if (options.length > 0) {
        options.forEach(v => {
            const opt = document.createElement('option');
            opt.value = v; opt.textContent = v;
            viaggioSelect.appendChild(opt);
        });
        viaggioSelect.disabled = false;
    }
};

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    // 1. Gestione Login
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('username')?.value.trim().toLowerCase();
            const password = document.getElementById('password')?.value.trim();
            const btn = loginForm.querySelector('.btn-primary');
            const alertEl = document.getElementById('authAlert');

            if (!email || !password) return;

            btn.disabled = true;
            btn.innerHTML = 'Accesso in corso...';
            if (alertEl) { alertEl.style.display = 'none'; }

            try {
                if (typeof window.loginWithFirebase === 'function') {
                    await window.loginWithFirebase(email, password);
                    console.log("[Auth] Login avviato con successo.");
                } else {
                    throw new Error("Modulo Firebase non caricato correttamente.");
                }
            } catch (err) {
                console.error("[Auth] Errore di accesso:", err);
                if (alertEl) {
                    alertEl.style.display = 'block';
                    alertEl.style.background = '#fef2f2';
                    alertEl.style.color = '#991b1b';
                    alertEl.style.borderColor = '#fee2e2';
                    alertEl.textContent = "Errore: " + (err.code === 'auth/invalid-credential' ? 'Credenziali non valide' : err.message);
                } else {
                    alert("Errore Accesso: " + err.message);
                }
                btn.disabled = false;
                btn.innerHTML = 'Accedi ora';
            }
        });
    }

    // 2. Popola Ore nelle select
    document.querySelectorAll('.hour-select').forEach(select => {
        for (let i = 0; i < 24; i++) {
            const opt = document.createElement('option');
            const val = i.toString().padStart(2, '0');
            opt.value = val; opt.textContent = val;
            select.appendChild(opt);
        }
    });

    // Event Listeners
    document.getElementById('clienteSelect')?.addEventListener('change', window.updateViaggi);
    document.getElementById('kmArrivo')?.addEventListener('input', calcolaTutto);
    document.getElementById('oraFineHH')?.addEventListener('change', calcolaTutto);
    document.getElementById('oraFineMM')?.addEventListener('change', calcolaTutto);
    
    const dataInput = document.getElementById('data');
    if (dataInput && !dataInput.value) {
        dataInput.value = new Date().toISOString().split('T')[0];
    }

    // PWA: Registrazione Service Worker + gestione aggiornamenti
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('./sw.js').then(reg => {
            console.log('[SW] Registrato correttamente.');

            // Se c'Ã¨ giÃ  un SW in attesa (tab rimasto aperto durante aggiornamento)
            // â†’ invia subito SKIP_WAITING per forzare l'attivazione
            if (reg.waiting) {
                console.log('[SW] SW in attesa trovato â€” invio SKIP_WAITING.');
                reg.waiting.postMessage({ type: 'SKIP_WAITING' });
                showUpdateToast(reg);
            }

            reg.addEventListener('updatefound', () => {
                const newWorker = reg.installing;
                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        console.log('[SW] Nuova versione installata, mostro banner aggiornamento.');
                        showUpdateToast(reg);
                    }
                });
            });
        }).catch(err => {
            console.error('[SW] Errore registrazione:', err);
        });

        // âš¡ CRITICO: Quando il nuovo SW prende il controllo, ricarica la pagina automaticamente
        // Questo garantisce che il telefono non rimanga su una versione vecchia.
        let swRefreshing = false;
        navigator.serviceWorker.addEventListener('controllerchange', () => {
            if (swRefreshing) return;
            swRefreshing = true;
            console.log('[SW] Nuova versione attiva â€” ricarico la pagina...');
            window.location.reload();
        });
    }
});

function showUpdateToast(reg) {
    // Evita duplicati se il toast Ã¨ giÃ  presente
    if (document.getElementById('sw-update-toast')) return;

    const toast = document.createElement('div');
    toast.id = 'sw-update-toast';
    toast.className = 'sw-update-toast show';
    toast.innerHTML = `
        <div style="flex:1;">ðŸ†• Nuova versione disponibile (v${APP_VERSION})</div>
        <button class="btn-update" id="btn-sw-update">Aggiorna ora</button>
    `;
    document.body.appendChild(toast);

    // Il pulsante invia SKIP_WAITING al SW in attesa, poi il controllerchange ricarica
    document.getElementById('btn-sw-update').addEventListener('click', () => {
        if (reg.waiting) {
            console.log('[SW] Utente ha cliccato Aggiorna â€” invio SKIP_WAITING.');
            reg.waiting.postMessage({ type: 'SKIP_WAITING' });
        } else {
            // Fallback: nessun SW in attesa, ricarica direttamente
            window.location.reload();
        }
    });
}

// --- AUTH HOOKS ---
window.onUserProfileLoaded = (user) => {
    const autistaEl = document.getElementById('autistaNome');
    if (autistaEl) autistaEl.value = user.nome || '';
    
    const dashBtn = document.getElementById('dashboardBtn');
    const role = (user.ruolo || 'autista').toLowerCase();
    if (dashBtn) dashBtn.style.display = (role === 'amministratore' || role === 'impiegata') ? 'flex' : 'none';

    // Inizializza i menu a tendina dinamici se i dati sono giÃ  pronti
    if (typeof window.renderMezziInserimento === 'function') window.renderMezziInserimento();
    if (typeof window.renderClientiInserimento === 'function') window.renderClientiInserimento();

    // Se siamo in inserimento e c'Ã¨ una bozza, mostriamo il modale
    if (document.getElementById('presenzeForm') && sessionStorage.getItem('currentDraft')) {
        document.getElementById('recoveryTripModal')?.classList.add('active');
    }
};

window.closeConfirmModal = () => document.getElementById('confirmModal')?.classList.remove('active');
