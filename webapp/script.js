const APP_VERSION = "1.1";
const GESTIONE_URL = "https://script.google.com/macros/s/AKfycbyPS-eF42oyNCzAlwu4n6mOcMKZYvBlkyuVfKgLFi6wmPSM77FjvdjwhBVaqE2frT6LVg/exec";
const IMPOSTAZIONI_URL = GESTIONE_URL;
const GOOGLE_SHEET_URL = GESTIONE_URL;

// --- GESTIONE VERSIONE E FORZATURA REFRESH ---
(function checkVersion() {
    // 1. Registrazione Service Worker
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('./sw.js')
                .then(reg => console.log('Service Worker registrato con successo:', reg.scope))
                .catch(err => console.error('Errore registrazione Service Worker:', err));
        });
    }

    const localVersion = localStorage.getItem('app_version');
    if (localVersion !== APP_VERSION) {
        console.log(`Nuova versione rilevata (da ${localVersion || 'N/A'} a ${APP_VERSION}). Aggiornamento cache...`);
        localStorage.setItem('app_version', APP_VERSION);
        
        // Pulizia selettiva della cache locale
        const currentUser = localStorage.getItem('currentUser');
        const bioUser = localStorage.getItem('biometric_linked_user');
        
        localStorage.clear();
        
        if (currentUser) localStorage.setItem('currentUser', currentUser);
        if (bioUser) localStorage.setItem('biometric_linked_user', bioUser);
        localStorage.setItem('app_version', APP_VERSION);
        
        // Forza ricaricamento bypassando cache
        window.location.reload(true);
    }
})();

// --- SINCRONIZZAZIONE DATI INIZIALE ---
// Funzione di base che decide COME sincronizzare (Firebase o, in futuro, Apps Script)
async function baseSyncFromCloud() {
    if (typeof window.syncFromFirebase === 'function') {
        // Usa Firebase come sorgente principale se disponibile
        await window.syncFromFirebase();
    } else {
        try {
            console.log("Sincronizzazione cloud legacy non configurata (nessun syncFromFirebase disponibile).");
            // Qui in passato poteva esserci una chiamata a Google Apps Script (GOOGLE_SHEET_URL)
            // Al momento non facciamo nulla per evitare errori ricorsivi.
        } catch (e) {
            console.error("Errore sincronizzazione cloud legacy:", e);
        }
    }
}

// Esegui sincronizzazione intelligente all'avvio
async function smartSync() {
    const hasClienti = localStorage.getItem('lista_clienti');
    const hasAutisti = localStorage.getItem('lista_autisti');
    const hasMezzi = localStorage.getItem('lista_mezzi');

    // Se manca anche solo una delle liste fondamentali, sincronizza tutto
    if (!hasClienti || !hasAutisti || !hasMezzi) {
        console.log("Dati locali incompleti, avvio sincronizzazione da Cloud...");
        await baseSyncFromCloud();
    } else {
        console.log("Dati (Clienti, Autisti, Mezzi) presenti localmente. Uso cache cloud.");
    }
}

// Espone la smartSync come API globale per le altre parti dell'app
window.syncFromCloud = smartSync;

// Esegui sincronizzazione all'avvio
smartSync();

document.addEventListener('DOMContentLoaded', () => {
    // 0. Gestione Visibilità Pulsanti Dashboard/Admin
    const lsSession = localStorage.getItem('currentUser');
    if (lsSession) {
        const sessionObj = JSON.parse(lsSession);
        const role = (sessionObj.ruolo || '').toLowerCase();
        if (role === 'amministratore' || role === 'impiegata') {
            const dashBtn = document.getElementById('dashboardBtn');
            if (dashBtn) dashBtn.style.display = 'flex';
        }
    }

    // 1. Gestione Login Autisti
    const loginForm = document.getElementById('loginForm');
    const biometricBtn = document.getElementById('biometricBtn');
    const bioModal = document.getElementById('biometricActiveModal');

    if (loginForm) {
        // Controllo supporto biometria e link esistente
        const linkedUser = localStorage.getItem('biometric_linked_user');
        if (linkedUser && biometricBtn) {
            biometricBtn.style.display = 'flex';
            biometricBtn.onclick = loginWithBiometrics;
        }
        const recoveryLink = document.getElementById('recoveryLink');
        const usernameInput = document.getElementById('username');

        if (usernameInput && recoveryLink) {
            usernameInput.addEventListener('input', () => {
                const user = usernameInput.value.trim().toLowerCase();
                const autisti = JSON.parse(localStorage.getItem('lista_autisti') || '[]');
                const found = autisti.find(a => a.nome.toLowerCase() === user && a.ruolo === 'amministratore');
                recoveryLink.style.display = found ? 'block' : 'none';
            });
        }

        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const rawUsername = document.getElementById('username').value.trim();
            const passwordInput = document.getElementById('password').value.trim();
            const btn = loginForm.querySelector('.btn-primary');

            // Prima del login, tentiamo una sync rapida (automaticamente userà Firebase se caricato)
            await syncFromCloud();

            const autisti = JSON.parse(localStorage.getItem('lista_autisti') || '[]');
            console.log("Tentativo login per:", rawUsername);

            // Ricerca dell'utente
            const autistaTrovato = autisti.find(a =>
                a.nome.toLowerCase() === rawUsername.toLowerCase() ||
                (rawUsername.toLowerCase().length > 3 && a.nome.toLowerCase().includes(rawUsername.toLowerCase()))
            );

            if (autistaTrovato && autistaTrovato.password === passwordInput) {
                const userObj = {
                    nome: autistaTrovato.nome,
                    ruolo: autistaTrovato.ruolo || 'autista',
                    tipoTurno: autistaTrovato.tipoTurno || 'giornata',
                    canElevate: autistaTrovato.canElevate || false,
                    email: autistaTrovato.email || ''
                };
                localStorage.setItem('currentUser', JSON.stringify(userObj));

                btn.innerHTML = 'Accesso in corso...';
                setTimeout(() => {
                    // Dopo il login, se la biometria non è attiva, proponiamola
                    if (!localStorage.getItem('biometric_linked_user')) {
                        if (bioModal) bioModal.classList.add('active');
                        else finalizeLogin(userObj);
                    } else {
                        finalizeLogin(userObj);
                    }
                }, 800);
            } else {
                alert("Credenziali non valide o utente non trovato.");
            }
        });
    }

    // 2. Gestione Form Inserimento (Wizard)
    const presenzeForm = document.getElementById('presenzeForm');
    if (presenzeForm) {
        const autistaNomeEl = document.getElementById('autistaNome');
        let sessionNome = 'Sconosciuto';
        const lsSession = localStorage.getItem('currentUser');
        const sessionObj = lsSession ? JSON.parse(lsSession) : {};
        sessionNome = sessionObj.nome || 'Sconosciuto';
        if (autistaNomeEl) autistaNomeEl.value = sessionNome;

        // Popolamento Automezzi
        window.renderMezziInserimento = function() {
            if (!automezzoSelect) return;
            const currentVal = automezzoSelect.value;
            const DEFAULT_MEZZI = [{ targa: 'FJ638LN' }, { targa: 'FD788RT' }, { targa: 'GB969FN' }, { targa: 'GF929KT' }];
            const mezzi = JSON.parse(localStorage.getItem('lista_mezzi') || JSON.stringify(DEFAULT_MEZZI));
            
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
                const clienti = JSON.parse(localStorage.getItem('lista_clienti') || '[]');
                
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
            const clienti = JSON.parse(localStorage.getItem('lista_clienti') || '[]');
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
            // Aggiungiamo opzioni speciali in testa
            if (id === 'mattinaInizioHH') {
                const opt = document.createElement('option');
                opt.value = "SOLO_POM"; opt.textContent = "Solo Pomeriggio";
                select.appendChild(opt);
            }
            if (id === 'pomeriggioFineHH') {
                const opt = document.createElement('option');
                opt.value = "SOLO_MAT"; opt.textContent = "Solo Mattina";
                select.appendChild(opt);
            }

            for (let i = 0; i < 24; i++) {
                const opt = document.createElement('option');
                const val = i.toString().padStart(2, '0');
                opt.value = val;
                opt.textContent = val;
                select.appendChild(opt);
            }

            // Listener per forzare minuti a 00 se selezionata opzione speciale
            select.addEventListener('change', () => {
                const baseId = id.replace('HH', '');
                const mEl = document.getElementById(baseId + 'MM');
                if ((select.value === "SOLO_POM" || select.value === "SOLO_MAT") && mEl) {
                    mEl.value = "00";
                    mEl.disabled = true;
                } else if (mEl) {
                    mEl.disabled = false;
                }
            });
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

            localStorage.setItem(`draft_${sessionNome}`, JSON.stringify(draft));
        }

        function loadDraft() {
            const saved = localStorage.getItem(`draft_${sessionNome}`);
            if (saved) {
                const draft = JSON.parse(saved);
                if (draft.step > 1 && draft.step < 5) recoveryTripModal.classList.add('active');
            }
        }

        window.resumeDraft = () => {
            const saved = localStorage.getItem(`draft_${sessionNome}`);
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
            localStorage.removeItem(`draft_${sessionNome}`);
            recoveryTripModal.classList.remove('active');
            window.location.reload();
        };

        const step1Inputs = ['data', 'automezzo', 'clienteId', 'kmPartenza', 'mattinaInizio'];
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
                    cliente: document.getElementById('cliente').value,
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

            // Logica Calcolo con Eccezioni "Solo Mattina/Pomeriggio"
            const isSoloPom = (mI === 'SOLO_POM:00');
            const isSoloMat = (pF === 'SOLO_MAT:00');

            if (isSoloPom) {
                // Calcola solo pomeriggio
                if (pI && pF && pF !== 'SOLO_MAT:00') totalM = diffMin(pI, pF);
            } else if (isSoloMat) {
                // Calcola solo mattina
                if (mI && mF && mI !== 'SOLO_POM:00') totalM = diffMin(mI, mF);
            } else {
                // Calcolo standard a intervalli
                if (mI && mF) totalM += diffMin(mI, mF);
                if (pI && pF) totalM += diffMin(pI, pF);

                // Caso turno unico (senza pause centrali)
                if (mI && pF && !mF && !pI) {
                    totalM = diffMin(mI, pF);
                }
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

            const isSoloPom = (mI === 'SOLO_POM:00');
            const isSoloMat = (pF === 'SOLO_MAT:00');

            if (!isSoloPom && !isSoloMat) {
                // Regola della coppia: se inserisci uno, devi inserire l'altro (solo se non è un turno unico o speciale)
                if ((mF && !pI) || (!mF && pI)) {
                    alert("Errore: Se inserisci una pausa (Mattina Fine o Pomeriggio Inizio), devi compilarle entrambe.");
                    return;
                }
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
                cliente: document.getElementById('cliente').value,
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

                localStorage.removeItem(`draft_${sessionNome}`);
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
                localStorage.removeItem(`draft_${sessionNome}`);
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

    // 3. Ruoli e Protezione
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
    const userRole = currentUser.ruolo || 'autista';
    const adminBtn = document.getElementById('adminSettingsBtn');
    if (adminBtn) {
        if (userRole === 'autista') adminBtn.style.display = 'none';
        else adminBtn.onclick = () => window.location.href = 'impostazioni.html';
    }
    if (userRole === 'autista' && (window.location.pathname.includes('impostazioni.html') || window.location.pathname.includes('visualizzazione.html'))) {
        window.location.href = 'inserimento.html';
    }

    // --- FUNZIONI BIOMETRICHE ---
    window.closeBiometricModal = () => {
        if (bioModal) bioModal.classList.remove('active');
        const user = JSON.parse(localStorage.getItem('currentUser') || '{}');
        finalizeLogin(user);
    };

    window.setupBiometrics = async () => {
        try {
            // Generiamo un challenge fittizio (WebAuthn richiede un buffer)
            const challenge = new Uint8Array(32);
            window.crypto.getRandomValues(challenge);

            const user = JSON.parse(localStorage.getItem('currentUser') || '{}');

            const createCredentialOptions = {
                publicKey: {
                    challenge: challenge,
                    rp: { name: "Log Solution" },
                    user: {
                        id: new Uint8Array(16), // ID univoco fittizio
                        name: user.nome,
                        displayName: user.nome
                    },
                    pubKeyCredParams: [{ alg: -7, type: "public-key" }, { alg: -257, type: "public-key" }],
                    timeout: 60000,
                    attestation: "direct"
                }
            };

            await navigator.credentials.create(createCredentialOptions);

            // Se arriviamo qui, l'utente ha confermato con FaceID/TouchID
            localStorage.setItem('biometric_linked_user', user.nome);
            alert("Face ID attivato con successo!");
            closeBiometricModal();
        } catch (err) {
            console.error("Errore attivazione biometria:", err);
            alert("Non è stato possibile attivare il Face ID su questo dispositivo.");
            closeBiometricModal();
        }
    };

    async function loginWithBiometrics() {
        try {
            const linkedUser = localStorage.getItem('biometric_linked_user');
            if (!linkedUser) return;

            const challenge = new Uint8Array(32);
            window.crypto.getRandomValues(challenge);

            const getCredentialOptions = {
                publicKey: {
                    challenge: challenge,
                    timeout: 60000,
                    userVerification: "required"
                }
            };

            await navigator.credentials.get(getCredentialOptions);

            // Successo! Cerchiamo l'utente e logghiamo
            const autisti = JSON.parse(localStorage.getItem('lista_autisti') || '[]');
            const found = autisti.find(a => a.nome === linkedUser);

            if (found) {
                const userObj = {
                    nome: found.nome,
                    ruolo: found.ruolo || 'autista',
                    tipoTurno: found.tipoTurno || 'giornata',
                    canElevate: found.canElevate || false
                };
                localStorage.setItem('currentUser', JSON.stringify(userObj));
                finalizeLogin(userObj);
            }
        } catch (err) {
            console.error("Errore login biometrico:", err);
        }
    }

    function finalizeLogin(user) {
        if (!user.nome) return;
        const role = (user.ruolo || 'autista').toLowerCase();
        
        if (role === 'autista') {
            window.location.href = 'inserimento.html';
        } else if (role === 'amministratore' || role === 'impiegata') {
            window.location.href = 'dashboard.html';
        } else {
            // Default fall-back
            window.location.href = 'inserimento.html';
        }
    }
});

