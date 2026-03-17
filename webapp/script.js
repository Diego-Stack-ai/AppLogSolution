const APP_VERSION = "1.8";
const GESTIONE_URL = "https://script.google.com/macros/s/AKfycbyPS-eF42oyNCzAlwu4n6mOcMKZYvBlkyuVfKgLFi6wmPSM77FjvdjwhBVaqE2frT6LVg/exec";
const IMPOSTAZIONI_URL = GESTIONE_URL;
const GOOGLE_SHEET_URL = GESTIONE_URL;

// --- GESTIONE DATI IN MEMORIA E URL (NO PERSISTENZA) ---
window.appData = window.appData || {
    lista_clienti: [],
    lista_autisti: [],
    lista_mezzi: [],
    currentUser: {}
};

// La gestione della sessione è centralizzata in firebase-auth-sync.js via Auth State.


// Navigazione sicura iniettando lo stato nell'URL
window.navigateWithState = function(page) {
    window.location.href = page;
};

// Funzione mostrare/nascondere password
window.togglePasswordVisibility = function() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');
    console.log("Toggle password clicked. Current type:", passwordInput ? passwordInput.type : "null");
    
    if (!passwordInput || !toggleIcon) return;
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.textContent = 'visibility_off';
    } else {
        passwordInput.type = 'password';
        toggleIcon.textContent = 'visibility';
    }
};

// --- SINCRONIZZAZIONE DATI (FIREBASE -> MEMORY) ---
async function baseSyncFromCloud() {
    if (typeof window.syncFromFirebase === 'function') {
        await window.syncFromFirebase();
    }
}

async function smartSync() {
    // Senza localStorage, sincronizziamo sempre col Cloud all'avvio della sessione
    console.log("Inizializzazione dati in memoria...");
    await baseSyncFromCloud();
}

// Espone la smartSync come API globale
window.syncFromCloud = smartSync;
smartSync();

document.addEventListener('DOMContentLoaded', () => {
    // 0. Gestione Visibilità Pulsanti Dashboard/Admin spostata in onUserProfileLoaded globale sotto

    // 1. Gestione Login Autisti
    const loginForm = document.getElementById('loginForm');
    const biometricBtn = document.getElementById('biometricBtn');
    const bioModal = document.getElementById('biometricActiveModal');

    if (loginForm) {
        // Controllo supporto biometria e link esistente
        // Biometria rimossa per eliminare persistenza browser
        const biometricBtn = document.getElementById('biometricBtn');
        if (biometricBtn) biometricBtn.style.display = 'none';
        const usernameInput = document.getElementById('username');

        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            // Convertiamo in minuscolo per evitare errori di battitura/auto-maiuscole su mobile
            const email = document.getElementById('username').value.trim().toLowerCase();
            const password = document.getElementById('password').value.trim();
            const btn = loginForm.querySelector('.btn-primary');

            btn.disabled = true;
            btn.innerHTML = 'Accesso in corso...';

            console.log("Inizio processo di login...");
            try {
                await window.loginWithFirebase(email, password);
                console.log("Firebase Auth Successo. Caricamento profilo in corso tramite listener globale...");
            } catch (err) {
                console.error("Errore Login Form:", err);
                alert("Errore Accesso: " + err.message);
                btn.disabled = false;
                btn.innerHTML = 'Accedi ora';
            }
        });
    }

    // 2. Gestione Form Inserimento (Wizard)
    const presenzeForm = document.getElementById('presenzeForm');
    if (presenzeForm) {
        const autistaNomeEl = document.getElementById('autistaNome');
        let sessionNome = 'Sconosciuto';
        const sessionObj = window.appData.currentUser;
        if (sessionObj && sessionObj.nome) {
            if (autistaNomeEl) autistaNomeEl.value = sessionObj.nome;
        }

        // Popolamento Automezzi
        window.renderMezziInserimento = function() {
            const automezzoSelect = document.getElementById('automezzo');
            if (!automezzoSelect) return;
            const currentVal = automezzoSelect.value;
            const DEFAULT_MEZZI = [{ targa: 'FJ638LN' }, { targa: 'FD788RT' }, { targa: 'GB969FN' }, { targa: 'GF929KT' }];
            const mezzi = window.appData.lista_mezzi.length > 0 ? window.appData.lista_mezzi : DEFAULT_MEZZI;
            
            automezzoSelect.innerHTML = '<option value="">Seleziona targa...</option>';
            mezzi.forEach(m => {
                const opt = document.createElement('option');
                opt.value = m.targa;
                opt.textContent = m.modello ? `${m.targa} - ${m.modello}` : m.targa;
                automezzoSelect.appendChild(opt);
            });
            automezzoSelect.value = currentVal;
        }
        renderMezziInserimento();

        // --- CUSTOM TIME HELPERS ---
        function getTimeValue(id) {
            const h = document.getElementById(id + 'HH')?.value;
            const m = document.getElementById(id + 'MM')?.value;
            if (!h || !m) return "";
            return `${h}:${m}`;
        }

        function setTimeValue(id, val) {
            if (!val || !val.includes(':')) return;
            const [h, m] = val.split(':');
            const hEl = document.getElementById(id + 'HH');
            const mEl = document.getElementById(id + 'MM');
            if (hEl) hEl.value = h;
            if (mEl) mEl.value = m;
        }

        // --- RICERCA CLIENTI ---
        const clienteSearch = document.getElementById('clienteSearch');
        const clienteId = document.getElementById('clienteId');
        const clienteResults = document.getElementById('clienteResults');
        const clienteDettagli = document.getElementById('clienteDettagli');

        if (clienteSearch) {
            clienteSearch.addEventListener('input', () => {
                const query = clienteSearch.value.trim().toLowerCase();
                const clienti = window.appData.lista_clienti;
                
                if (query.length < 2) {
                    clienteResults.classList.remove('active');
                    return;
                }

                const filtered = clienti.filter(c => 
                    c.nome.toLowerCase().includes(query) || 
                    c.citta.toLowerCase().includes(query) ||
                    c.codiceLatte.toLowerCase().includes(query)
                ).slice(0, 10);

                if (filtered.length > 0) {
                    clienteResults.innerHTML = filtered.map(c => `
                        <div class="search-result-item" onclick="selectCliente('${c.nome.replace(/'/g, "\\'")}', '${c.codiceFrutta}_${c.codiceLatte}')">
                            <span class="name">${c.nome}</span>
                            <span class="sub">
                                <span style="color:var(--primary); font-weight:700;">[F: ${c.codiceFrutta}, L: ${c.codiceLatte}]</span> 
                                ${c.indirizzo} - ${c.citta}
                            </span>
                        </div>
                    `).join('');
                    clienteResults.classList.add('active');
                } else {
                    clienteResults.classList.remove('active');
                }
            });

            // Chiudi risultati se clicchi fuori
            document.addEventListener('click', (e) => {
                if (!clienteSearch.contains(e.target) && !clienteResults.contains(e.target)) {
                    clienteResults.classList.remove('active');
                }
            });
        }

        window.selectCliente = (nome, id) => {
            clienteSearch.value = nome;
            clienteId.value = id;
            clienteResults.classList.remove('active');
            mostraDettagliCliente(id);
            checkStep1();
            saveDraft();
        }

        function mostraDettagliCliente(id) {
            const clienti = window.appData.lista_clienti || [];
            const c = clienti.find(item => (item.codiceFrutta + "_" + item.codiceLatte) === id);
            
            if (c && clienteDettagli) {
                document.getElementById('detIndirizzo').textContent = c.indirizzo || '-';
                document.getElementById('detCitta').textContent = c.citta || '-';
                document.getElementById('detProv').textContent = c.provincia || '-';
                document.getElementById('detCap').textContent = c.cap || '-';
                document.getElementById('detEmail').textContent = c.email || '-';
                
                // Nuovi campi abilitati
                const extraInfo = `
                    <div style="grid-column: 1 / -1; border-top: 1px solid rgba(0,0,0,0.1); padding-top: 8px; margin-top: 5px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div><strong>Tipo Consegna:</strong> ${c.tipologiaConsegna || '-'}</div>
                        <div><strong>Orari:</strong> ${c.orarioMin || 'N.D.'} - ${c.orarioMax || 'N.D.'}</div>
                        <div><strong>Grado:</strong> ${c.tipologiaGrado || '-'}</div>
                        <div><strong>Codici:</strong> F: ${c.codiceFrutta || '-'} | L: ${c.codiceLatte || '-'}</div>
                    </div>
                `;
                
                // Aggiorna o crea il div extra
                let extraEl = document.getElementById('detExtra');
                if (!extraEl) {
                    extraEl = document.createElement('div');
                    extraEl.id = 'detExtra';
                    clienteDettagli.querySelector('div').appendChild(extraEl);
                }
                extraEl.innerHTML = extraInfo;

                const home = document.getElementById('detHome');
                if (c.homePage && c.homePage !== 'nan') {
                    home.href = c.homePage.startsWith('http') ? c.homePage : 'https://' + c.homePage;
                    home.style.display = 'inline';
                    home.textContent = c.homePage;
                } else {
                    home.style.display = 'none';
                    home.parentElement.style.display = 'none';
                }
                clienteDettagli.style.display = 'block';
            }
        }

        // Popola Ore (00-23)
        document.querySelectorAll('.hour-select').forEach(select => {
            const id = select.id;

            for (let i = 0; i < 24; i++) {
                const opt = document.createElement('option');
                const val = i.toString().padStart(2, '0');
                opt.value = val;
                opt.textContent = val;
                select.appendChild(opt);
            }
        });

        // --- LOGICA WIZARD ---
        let currentStep = 1;
        const totalSteps = 4;
        const btnStartTrip = document.getElementById('btnStartTrip');
        const confirmModal = document.getElementById('confirmModal');
        const btnConfirmSend = document.getElementById('btnConfirmSend');
        const recoveryTripModal = document.getElementById('recoveryTripModal');

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
            document.querySelectorAll('.step-container').forEach(c => c.classList.remove('active'));
            document.getElementById(`step-${currentStep}`).classList.add('active');

            for (let i = 1; i <= totalSteps; i++) {
                const dot = document.getElementById(`dot-${i}`);
                if (i < currentStep) { dot.classList.add('completed'); dot.innerHTML = '✓'; }
                else if (i === currentStep) { dot.classList.add('active'); dot.classList.remove('completed'); dot.innerHTML = i; }
                else { dot.classList.remove('active', 'completed'); dot.innerHTML = i; }
            }

            if (currentStep > 1) {
                document.querySelectorAll('#step-1 input, #step-1 select').forEach(el => {
                    el.classList.add('readonly-field');
                    el.readOnly = true;
                    if (el.tagName === 'SELECT') el.disabled = true;
                });
            } else {
                document.querySelectorAll('#step-1 input, #step-1 select').forEach(el => {
                    const isNotturnoDate = (el.id === 'data' && sessionObj.tipoTurno === 'notturno');
                    const isEditable = el.id !== 'autistaNome' && (el.id !== 'data' || isNotturnoDate);

                    if (isEditable) {
                        el.classList.remove('readonly-field');
                        el.readOnly = false;
                        if (el.tagName === 'SELECT') el.disabled = false;
                    } else {
                        el.classList.add('readonly-field');
                        el.readOnly = true;
                        if (el.tagName === 'SELECT') el.disabled = true;
                    }
                });
            }
            window.scrollTo({ top: 0, behavior: 'smooth' });
            calcolaTutto();
        }

        // --- BOZZE ---
        const timeFields = ['mattinaInizio', 'mattinaFine', 'pomeriggioInizio', 'pomeriggioFine'];

        function saveDraft() {
            const draft = { step: currentStep, data: {}, timestamp: new Date().getTime() };
            const ids = ['data', 'automezzo', 'clienteSearch', 'clienteId', 'kmPartenza', 'kmArrivo', 'importo', 'litri', 'nota'];

            ids.forEach(id => { const el = document.getElementById(id); if (el) draft.data[id] = el.value; });
            timeFields.forEach(id => { draft.data[id] = getTimeValue(id); });

            // Bozze disabilitate per rimuovere persistenza browser
            // window.appData.currentDraft = draft;
        }

        function loadDraft() {
            // Caricamento bozze rimosso
            // const saved = window.appData.currentDraft;
            if (saved) {
                const draft = JSON.parse(saved);
                if (draft.step > 1 && draft.step < 5) recoveryTripModal.classList.add('active');
            }
        }

        window.resumeDraft = () => {
            // Caricamento bozze rimosso
            // const saved = window.appData.currentDraft;
            if (saved) {
                const draft = JSON.parse(saved);
                Object.keys(draft.data).forEach(id => {
                    if (timeFields.includes(id)) {
                        setTimeValue(id, draft.data[id]);
                    } else {
                        const el = document.getElementById(id);
                        if (el) el.value = draft.data[id];
                    }
                });
                
                // Gestione specifica per il cliente
                if (draft.data.clienteId) {
                    mostraDettagliCliente(draft.data.clienteId);
                }

                currentStep = draft.step;
                updateStepUI();
            }
            recoveryTripModal.classList.remove('active');
        };

        window.discardDraft = () => {
            // Rimozione bozza disabilitata
            recoveryTripModal.classList.remove('active');
            window.location.reload();
        };

        const step1Inputs = ['data', 'automezzo', 'clienteSearch', 'kmPartenza', 'mattinaInizio'];
        step1Inputs.forEach(id => {
            if (id === 'mattinaInizio') {
                document.getElementById(id + 'HH')?.addEventListener('change', checkStep1);
                document.getElementById(id + 'MM')?.addEventListener('change', checkStep1);
            } else {
                const el = document.getElementById(id);
                if (el) el.addEventListener('input', checkStep1);
                if (el) el.addEventListener('change', checkStep1);
            }
        });

        function checkStep1() {
            const allFilled = step1Inputs.every(id => {
                if (id === 'mattinaInizio') return getTimeValue(id) !== '';
                const el = document.getElementById(id);
                return el && el.value.trim() !== '';
            });
            if (btnStartTrip) btnStartTrip.style.display = allFilled ? 'flex' : 'none';
        }
        checkStep1(); // Esegui subito al caricamento

        if (btnStartTrip) {
            btnStartTrip.onclick = async () => {
                // Salvataggio immediato al Cloud al CLICK di Inizia Viaggio
                const originalContent = btnStartTrip.innerHTML;
                btnStartTrip.innerHTML = '<span class="material-icons-round">sync</span> Invio...';
                btnStartTrip.disabled = true;

                const dataVal = document.getElementById('data').value;
                if (!dataVal || dataVal === "") {
                    alert("La data non è valida. Seleziona una data corretta.");
                    btnStartTrip.innerHTML = originalContent;
                    btnStartTrip.disabled = false;
                    return;
                }

                const payload = {
                    action: "save_turn",
                    data: dataVal,
                    autista: sessionNome,
                    automezzo: document.getElementById('automezzo').value,
                    cliente: document.getElementById('clienteSearch')?.value || '',
                    km_partenza: document.getElementById('kmPartenza').value,
                    mattina_inizio: getTimeValue('mattinaInizio'),
                    status: "INIZIATO",
                    timestamp: new Date().toLocaleString()
                };

                try {
                    await fetch(GOOGLE_SHEET_URL, {
                        method: 'POST',
                        mode: 'no-cors',
                        body: JSON.stringify(payload)
                    });
                } catch (e) {
                    console.log("Invio inizio turno (ignore CORS)");
                }

                btnStartTrip.innerHTML = originalContent;
                btnStartTrip.disabled = false;
                nextStep(2);
            };
        }
        window.closeConfirmModal = () => confirmModal.classList.remove('active');

        // --- CALCOLI ---
        const fldCalcolo = ['kmPartenza', 'kmArrivo'];
        fldCalcolo.forEach(f => { const el = document.getElementById(f); if (el) el.addEventListener('input', calcolaTutto); });

        document.querySelectorAll('.hour-select, .min-select').forEach(s => {
            s.addEventListener('change', calcolaTutto);
        });

        function calcolaTutto() {
            const kmP = parseFloat(document.getElementById('kmPartenza').value) || 0;
            const kmA = parseFloat(document.getElementById('kmArrivo').value) || 0;
            document.getElementById('deltaKm').value = (kmA - kmP) > 0 ? (kmA - kmP) : '-';

            const mI = getTimeValue('mattinaInizio');
            const mF = getTimeValue('mattinaFine');
            const pI = getTimeValue('pomeriggioInizio');
            const pF = getTimeValue('pomeriggioFine');

            let totalM = 0;

            // Calcolo standard a intervalli
            if (mI && mF) totalM += diffMin(mI, mF);
            if (pI && pF) totalM += diffMin(pI, pF);

            // Caso turno unico (senza pause centrali)
            if (mI && pF && !mF && !pI) {
                totalM = diffMin(mI, pF);
            }

            if (totalM > 0) {
                const ordM = Math.min(totalM, 480); // Limite 8 ore (480 minuti)
                const straM = Math.max(0, totalM - 480);

                document.getElementById('totaleOre').value = formatHHMM(totalM);
                document.getElementById('oreOrdinarie').value = formatHHMM(ordM);
                document.getElementById('oreStraordinario').value = formatHHMM(straM);
            } else {
                ['totaleOre', 'oreOrdinarie', 'oreStraordinario'].forEach(id => document.getElementById(id).value = '-');
            }
            saveDraft(); // Salva bozza ad ogni calcolo/modifica
        }

        function formatHHMM(min) {
            if (min <= 0) return "0:00";
            const h = Math.floor(min / 60);
            const m = min % 60;
            return `${h}:${m.toString().padStart(2, '0')}`;
        }

        function diffMin(s, e) {
            const [h1, m1] = s.split(':').map(Number);
            const [h2, m2] = e.split(':').map(Number);
            return Math.max(0, (h2 * 60 + m2) - (h1 * 60 + m1));
        }

        // --- DATE ---
        const dataInput = document.getElementById('data');
        const nomeGiorno = document.getElementById('nomeGiorno');
        if (dataInput) {
            if (!dataInput.value) dataInput.value = new Date().toISOString().split('T')[0];
            if (sessionObj.tipoTurno === 'notturno') {
                dataInput.readOnly = false;
                dataInput.classList.remove('readonly-field');
            }
            dataInput.addEventListener('change', updateDayName);
            updateDayName();
        }
        function updateDayName() {
            if (dataInput.value) {
                const d = new Date(dataInput.value);
                nomeGiorno.textContent = new Intl.DateTimeFormat('it-IT', { weekday: 'long' }).format(d);
            }
        }

        // --- INVIO ---
        presenzeForm.addEventListener('submit', (e) => {
            e.preventDefault();

            // Validazione campi obbligatori per la chiusura (Step 4)
            const kmA = document.getElementById('kmArrivo').value.trim();
            const mF = getTimeValue('mattinaFine');
            const pF = getTimeValue('pomeriggioFine');

            if (!kmA) {
                alert("Errore: I KM di arrivo sono obbligatori per chiudere il turno.");
                return;
            }

            const mI = getTimeValue('mattinaInizio');
            const pI = getTimeValue('pomeriggioInizio');

            // Regola della coppia: se inserisci uno, devi inserire l'altro (solo se non è un turno unico o speciale)
            if ((mF && !pI) || (!mF && pI)) {
                alert("Errore: Se inserisci una pausa (Mattina Fine o Pomeriggio Inizio), devi compilarle entrambe.");
                return;
            }

            if (!pF) {
                alert("Errore: L'orario di fine turno è obbligatorio.");
                return;
            }

            confirmModal.classList.add('active');
        });

        btnConfirmSend.onclick = async () => {
            confirmModal.classList.remove('active');
            const btn = presenzeForm.querySelector('.btn-save');
            const originalText = btn.innerHTML;
            btn.innerHTML = 'Invio...'; btn.disabled = true;

            const payload = {
                action: "save_turn",
                data: dataInput.value,
                autista: sessionNome,
                automezzo: document.getElementById('automezzo').value,
                cliente: document.getElementById('clienteSearch')?.value || '',
                km_partenza: document.getElementById('kmPartenza').value,
                km_arrivo: document.getElementById('kmArrivo').value,
                delta_km: document.getElementById('deltaKm').value,
                mattina_inizio: getTimeValue('mattinaInizio'),
                mattina_fine: getTimeValue('mattinaFine'),
                pomeriggio_inizio: getTimeValue('pomeriggioInizio'),
                pomeriggio_fine: getTimeValue('pomeriggioFine'),
                ore_ordinarie: document.getElementById('oreOrdinarie').value,
                ore_straordinarie: document.getElementById('oreStraordinario').value,
                ore_totali: document.getElementById('totaleOre').value,
                importo: document.getElementById('importo').value,
                litri: document.getElementById('litri').value,
                nota: document.getElementById('nota').value,
                status: "COMPLETATO",
                timestamp: new Date().toLocaleString()
            };

            try {
                await fetch(GOOGLE_SHEET_URL, {
                    method: 'POST',
                    mode: 'no-cors',
                    body: JSON.stringify(payload)
                });

                // Bozze disabilitate
                btn.innerHTML = 'Turno Inviato ✓';
                btn.style.background = 'var(--success)';
                setTimeout(() => {
                    presenzeForm.reset();
                    if (autistaNomeEl) autistaNomeEl.value = sessionNome;
                    currentStep = 1; updateStepUI();
                    btn.innerHTML = originalText; btn.style.background = ''; btn.disabled = false;
                }, 2500);
            } catch (err) {
                console.error("Errore tecnico (CORS?), ma il dato potrebbe essere partito:", err);
                // Bozze disabilitate
                btn.innerHTML = 'Inviato ✓';
                btn.style.background = 'var(--success)';
                setTimeout(() => {
                    presenzeForm.reset();
                    if (autistaNomeEl) autistaNomeEl.value = sessionNome;
                    currentStep = 1; updateStepUI();
                    btn.innerHTML = originalText; btn.style.background = ''; btn.disabled = false;
                }, 2500);
            }
        };


        loadDraft();
    }

    // 3. Ruoli e Protezione Centralizzata in firebase-auth-sync.js
    // Non aggiungere redirect qui per evitare race conditions con il caricamento del profilo.
});

// --- SERVICE WORKER REGISTRATION & UPDATE NOTIFICATION ---
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js').then((reg) => {
            console.log('Service Worker registrato con successo.');

            // Controllo se c'è già un aggiornamento in attesa (es. download completato in precedenza)
            if (reg.waiting) {
                showUpdateToast(reg);
            }

            reg.addEventListener('updatefound', () => {
                const newWorker = reg.installing;
                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        // Nuovo contenuto disponibile!
                        showUpdateToast(reg);
                    }
                });
            });
        }).catch((err) => {
            console.error('Errore registrazione Service Worker:', err);
        });
    });

    let refreshing = false;
    navigator.serviceWorker.addEventListener('controllerchange', () => {
        if (refreshing) return;
        window.location.reload();
        refreshing = true;
    });
}

function showUpdateToast(reg) {
    const toast = document.createElement('div');
    toast.className = 'sw-update-toast';
    toast.innerHTML = `
        <div style="flex:1;">Nuova versione disponibile!</div>
        <button class="btn-update" id="sw-update-btn">Aggiorna</button>
    `;
    document.body.appendChild(toast);

    // Animazione entrata
    setTimeout(() => toast.classList.add('show'), 100);

    document.getElementById('sw-update-btn').onclick = () => {
        if (reg.waiting) {
            reg.waiting.postMessage('SKIP_WAITING');
        }
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400);
    };
}

// --- HOOK GLOBALE CARICAMENTO PROFILO ---
// Chiamato da firebase-auth-sync.js appena il profilo Firestore è pronto.
// Usa un delay minimo su mobile per attendere che il DOM sia completamente renderizzato.
window.onUserProfileLoaded = function(user) {
    console.log("Global Profile Hook: dati pronti per", user.nome, "[", user.ruolo, "]");

    const applyProfileToUI = () => {
        // 1. Aggiorna saluto utente (dashboard e pagine admin)
        const greetingEl = document.getElementById('userGreeting');
        if (greetingEl && user.nome) {
            greetingEl.textContent = user.nome;
            console.log("UI: userGreeting aggiornato con", user.nome);
        }

        // 2. Aggiorna nome autista nel form inserimento
        const autistaNomeEl = document.getElementById('autistaNome');
        if (autistaNomeEl && user.nome) {
            autistaNomeEl.value = user.nome;
            console.log("UI: autistaNome aggiornato con", user.nome);
        }

        // 3. Mostra pulsante dashboard solo per admin/impiegata
        const role = (user.ruolo || 'autista').toLowerCase();
        const dashBtn = document.getElementById('dashboardBtn');
        if (dashBtn) {
            dashBtn.style.display = (role === 'amministratore' || role === 'impiegata') ? 'flex' : 'none';
        }
    };

    // Se il DOM è già pronto eseguiamo subito, altrimenti aspettiamo
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        // Piccolo delay per sincronizzare il rendering su mobile (iOS/Android)
        setTimeout(applyProfileToUI, 150);
    } else {
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(applyProfileToUI, 150);
        });
    }
};

document.addEventListener('click', (e) => {
    const logoutBtn = e.target.closest('.logout-btn[title="Esci"], .logout-link');
    if (logoutBtn) {
        e.preventDefault();
        if (confirm("Sei sicuro di voler uscire?")) {
            if (typeof window.logoutFirebase === 'function') {
                window.logoutFirebase();
            } else {
                window.location.replace('login.html');
            }
        }
    }
});

// --- GESTIONE VISIBILITÀ INTERFACCIA (LANDING VS APP) ---
const handleInterfaceVisibility = () => {
    const body = document.body;
    // Rileva se siamo in landing o home tramite attributo data-page o URL
    const currentPage = body.getAttribute('data-page') || 
                       (window.location.pathname.endsWith('index.html') || window.location.pathname === '/' ? 'landing' : '');

    if (currentPage === 'home' || currentPage === 'landing') {
        body.classList.add('hide-nav');
    } else {
        body.classList.remove('hide-nav');
    }
};

// Eseguiamo immediatamente e anche al caricamento per sicurezza
handleInterfaceVisibility();
document.addEventListener('DOMContentLoaded', handleInterfaceVisibility);
