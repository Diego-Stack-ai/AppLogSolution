# -*- coding: utf-8 -*-
import re

with open('g:/Il mio Drive/App/AppLogSolutionsWeb/frontend/inserimento.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add modal HTML right after the confirmModal
modal_html = """
    <!-- Modal Gestione Anomalia Turno -->
    <div id="anomalyModal" class="modal-overlay">
        <div class="modal-content">
            <span class="material-icons-round modal-icon" style="color: #f59e0b;">warning</span>
            <h3>Turno Precedente Sospeso</h3>
            <p style="font-size: 14px; color: var(--text-muted); margin-bottom: 20px;">
                Il sistema ha rilevato un turno iniziato in data <b id="anomalyDateStr"></b> e non ancora chiuso.
                <br><br>
                Come vuoi procedere?
            </p>
            <div style="display:flex; flex-direction:column; gap:12px;">
                <button id="btnAnomalyNight" class="btn-primary" style="background:#0f172a;">
                    Sto chiudendo il turno di ieri (Turno Notturno)
                </button>
                <button id="btnAnomalyForgot" class="btn-primary" style="background:#fef2f2; color:#ef4444; border: 1px solid #ef4444; box-shadow:none;">
                    Ho dimenticato di chiuderlo (Annulla Turno)
                </button>
            </div>
        </div>
    </div>
"""

if "anomalyModal" not in content:
    content = content.replace('    <script src="script.js?v=2.72"></script>', modal_html + '\n    <script src="script.js?v=2.72"></script>')

# 2. Add imports
content = content.replace('import { saveTrip } from "./firestore-service.js?v=2.72";', 
                          'import { saveTrip, checkPendingTrip, closeTripWithAnomaly } from "./firestore-service.js?v=2.72";')

# 3. Add JS logic
js_logic = """
        // GESTIONE TURNI SOSPESI
        let currentPendingTrip = null;

        auth.onAuthStateChanged(async (user) => {
            if (user) {
                // Check pending trips on load
                const pendingTrip = await checkPendingTrip();
                if (pendingTrip) {
                    currentPendingTrip = pendingTrip;
                    const tripDate = pendingTrip.data;
                    const today = document.getElementById('data').value; // already populated by script.js with today's date

                    if (tripDate === today) {
                        // Stesso giorno, ripristina la schermata
                        restorePendingTrip(pendingTrip);
                    } else {
                        // Giorno precedente, mostra modale anomalia
                        document.getElementById('anomalyDateStr').innerText = tripDate;
                        document.getElementById('anomalyModal').classList.add('active');
                    }
                }
            }
        });

        function restorePendingTrip(trip) {
            sessionStorage.setItem('currentTripId', trip.id);
            // Popola i campi principali
            if(trip.data) document.getElementById('data').value = trip.data;
            if(trip.automezzo) document.getElementById('automezzo').value = trip.automezzo;
            if(trip.cliente) document.getElementById('clienteSelect').value = trip.cliente;
            if(trip.viaggio) {
                // Potrebbe dover essere aggiunto alle options dinamicamente o ritardato, ma se cliente esiste, viaggio c'è
                setTimeout(() => {
                    document.getElementById('viaggioSelect').value = trip.viaggio;
                    checkStep1();
                }, 500);
            }
            if(trip.kmPartenza) document.getElementById('kmPartenza').value = trip.kmPartenza;
            if(trip.mattinaInizio) {
                const parts = trip.mattinaInizio.split(':');
                if(parts.length === 2) {
                    document.getElementById('mattinaInizioHH').value = parts[0];
                    document.getElementById('mattinaInizioMM').value = parts[1];
                }
            }

            // Manda allo step 2
            btnStartTrip.innerHTML = '<span class="material-icons-round">gps_fixed</span> Tracking Attivo (Ripristinato)';
            btnStartTrip.disabled = true;
            btnStartTrip.style.display = 'flex';
            setTimeout(() => { window.nextStep(2); }, 300);
        }

        document.getElementById('btnAnomalyNight').onclick = () => {
            document.getElementById('anomalyModal').classList.remove('active');
            restorePendingTrip(currentPendingTrip);
        };

        document.getElementById('btnAnomalyForgot').onclick = async () => {
            const btn = document.getElementById('btnAnomalyForgot');
            btn.innerHTML = 'Annullamento in corso...';
            btn.disabled = true;
            
            await closeTripWithAnomaly(currentPendingTrip);
            
            alert("Turno chiuso con anomalia e notificato all'ufficio. Ora puoi inserire il nuovo turno di oggi.");
            
            sessionStorage.removeItem('currentTripId');
            sessionStorage.removeItem('currentDraft');
            window.location.reload();
        };
"""

if "currentPendingTrip" not in content:
    # insert inside the module script after const btnConfirmSend
    content = content.replace("const btnConfirmSend = document.getElementById('btnConfirmSend');", 
                              "const btnConfirmSend = document.getElementById('btnConfirmSend');\n" + js_logic)


with open('g:/Il mio Drive/App/AppLogSolutionsWeb/frontend/inserimento.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("inserimento.html updated successfully!")
