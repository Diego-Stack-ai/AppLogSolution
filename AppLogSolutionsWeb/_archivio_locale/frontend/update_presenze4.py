import re

file_path = r"g:\Il mio Drive\App\AppLogSolutionsWeb\frontend\presenze.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_render_calendar = r"""        // Genera tutti i giorni del mese selezionato
        function renderCalendar(presenzeMap) {
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';

            if (!selectedMonth) return;

            const [year, month] = selectedMonth.split('-').map(Number);
            const numDays = new Date(year, month, 0).getDate();
            const giorniSettimana = ['Domenica', 'Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato'];

            let totalOre = 0.0;
            let totalOrd = 0.0;
            let totalExtra = 0.0;
            let totalDeltaKm = 0.0;
            let totalImporto = 0.0;
            let totalLitri = 0.0;

            const isTutti = selectedEmployee.id === 'tutti';
            const forceFourCols = isTutti || selectedEmployee.ruolo === 'amministratore' || selectedEmployee.ruolo === 'impiegata';

            const tableHeadTr = document.getElementById('tableHeadTr');
            let headerHtml = `
                <th>Data</th>
                <th>Cliente</th>
                <th style="text-align:right;">Km<br>Part.</th>
                <th style="text-align:right;">Km<br>Arr.</th>
                <th style="text-align:right;">Delta<br>Km</th>
            `;
            if (forceFourCols) {
                headerHtml += `
                    <th style="text-align:center;">Iniz<br>M.</th>
                    <th style="text-align:center;">Fine<br>M.</th>
                    <th style="text-align:center;">Iniz<br>P.</th>
                    <th style="text-align:center;">Fine<br>P.</th>
                `;
            } else {
                headerHtml += `
                    <th style="text-align:center;">Inizio</th>
                    <th style="text-align:center;">Fine</th>
                `;
            }
            headerHtml += `
                <th style="text-align:right;">Tot.<br>Ore</th>
                <th style="text-align:right;">Ord.</th>
                <th style="text-align:right;">Straord.</th>
                <th style="text-align:center;">Azione</th>
            `;
            if (tableHeadTr) tableHeadTr.innerHTML = headerHtml;

            // Determine which days to render
            let startDay = 1;
            let endDay = numDays;

            if (currentViewMode === 'giorno') {
                if (!currentSubFilter) {
                    tbody.innerHTML = `<tr><td colspan="17" style="text-align:center; padding: 32px; color: var(--text-muted);">Seleziona un giorno dai filtri qui sopra.</td></tr>`;
                    document.getElementById('tableFoot').style.display = 'none';
                    resetSummary();
                    return;
                }
                startDay = parseInt(currentSubFilter);
                endDay = startDay;
            } else if (currentViewMode === 'settimana') {
                if (!currentSubFilter) {
                    tbody.innerHTML = `<tr><td colspan="17" style="text-align:center; padding: 32px; color: var(--text-muted);">Seleziona una settimana dai filtri qui sopra.</td></tr>`;
                    document.getElementById('tableFoot').style.display = 'none';
                    resetSummary();
                    return;
                }
                const activeBtn = document.querySelector(`.sub-filter-btn[data-val="${currentSubFilter}"]`);
                if (activeBtn) {
                    startDay = parseInt(activeBtn.dataset.start);
                    endDay = parseInt(activeBtn.dataset.end);
                }
            }

            const autistiToRender = isTutti ? (window.appData.lista_autisti || []).sort((a,b)=>(a.nome||'').localeCompare(b.nome||'')) : [selectedEmployee];

            autistiToRender.forEach(autista => {
                const isAdmin = autista.ruolo === 'amministratore' || autista.ruolo === 'impiegata';
                const defaultDoubleShift = isAdmin;

                if (isTutti) {
                    const sepTr = document.createElement('tr');
                    sepTr.className = 'employee-separator';
                    sepTr.innerHTML = `<td colspan="17">${autista.nome} ${autista.ruolo ? `(${autista.ruolo})` : ''}</td>`;
                    tbody.appendChild(sepTr);
                }

                for (let day = startDay; day <= endDay; day++) {
                    const dateStr = `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
                    const dt = new Date(year, month - 1, day);
                    const dayName = giorniSettimana[dt.getDay()];
                    const isWeekend = dt.getDay() === 0 || dt.getDay() === 6;

                    // Document ID in Firestore: {autistaId}_{data}
                    const docId = `${autista.id}_${dateStr}`;
                    const record = presenzeMap[docId] || {};

                    // Determina se abilitare l'orario sdoppiato
                    const isMagazzino = record.isMagazzino !== undefined ? record.isMagazzino : false;
                    const isDoubleShift = defaultDoubleShift || isMagazzino;

                    const tr = document.createElement('tr');
                    if (isWeekend) tr.classList.add('weekend');
                    tr.dataset.date = dateStr;
                    tr.dataset.docId = docId;
                    tr.dataset.autistaId = autista.id; // NEEDED FOR SAVE LATER!

                    const displayDate = dt.toLocaleDateString('it-IT', { day: '2-digit', month: '2-digit' });

                    tr.innerHTML = `
    <td><strong>${dayName}</strong><br><span style="font-size: 0.8em; color: #6b7280;">${displayDate}</span></td>
                        <td><input type="text" class="edit-input" data-field="cliente" value="${record.cliente || ''}" disabled></td>
                        <td><input type="number" class="edit-input num-input" data-field="kmPartenza" value="${record.kmPartenza || 0}" disabled onchange="onKmChange(this)"></td>
                        <td><input type="number" class="edit-input num-input" data-field="kmArrivo" value="${record.kmArrivo || 0}" disabled onchange="onKmChange(this)"></td>
                        <td><input type="number" class="edit-input num-input" data-field="kmDelta" value="${record.kmDelta || 0}" disabled readonly></td>
                        ${forceFourCols ? `
                            <td><input type="text" class="edit-input time-input" data-field="oraInizioM" value="${record.oraInizioM || ''}" disabled placeholder="00:00" onchange="onTimeChange(this)" style="${(!isAdmin && !isDoubleShift) ? 'background:#f1f5f9' : ''}"></td>
                            <td><input type="text" class="edit-input time-input" data-field="oraFineM" value="${record.oraFineM || ''}" disabled placeholder="00:00" onchange="onTimeChange(this)" style="${(!isAdmin && !isDoubleShift) ? 'background:#f1f5f9' : ''}"></td>
                            <td><input type="text" class="edit-input time-input" data-field="oraInizioP" value="${record.oraInizioP || ''}" disabled placeholder="00:00" onchange="onTimeChange(this)" style="display:${(isAdmin || isDoubleShift) ? 'block' : 'none'};"></td>
                            <td><input type="text" class="edit-input time-input" data-field="oraFineP" value="${record.oraFineP || ''}" disabled placeholder="00:00" onchange="onTimeChange(this)" style="display:${(isAdmin || isDoubleShift) ? 'block' : 'none'};"></td>
                        ` : `
                            <td>
                                <input type="text" class="edit-input time-input" data-field="oraInizioM" value="${record.oraInizioM || ''}" disabled placeholder="00:00" onchange="onTimeChange(this)">
                                <input type="text" class="edit-input time-input" data-field="oraInizioP" value="${record.oraInizioP || ''}" disabled placeholder="00:00" onchange="onTimeChange(this)" style="display:${isMagazzino ? 'block' : 'none'}; margin-top:4px; border-top:1px dashed #ccc; padding-top:4px;">
                            </td>
                            <td>
                                <input type="text" class="edit-input time-input" data-field="oraFineM" value="${record.oraFineM || ''}" disabled placeholder="00:00" onchange="onTimeChange(this)">
                                <input type="text" class="edit-input time-input" data-field="oraFineP" value="${record.oraFineP || ''}" disabled placeholder="00:00" onchange="onTimeChange(this)" style="display:${isMagazzino ? 'block' : 'none'}; margin-top:4px; border-top:1px dashed #ccc; padding-top:4px;">
                            </td>
                        `}
                        <td><input type="number" step="0.01" class="edit-input num-input" data-field="oreTotali" value="${record.oreTotali || 0}" disabled readonly></td>
                        <td><input type="number" step="0.01" class="edit-input num-input" data-field="oreOrdinarie" value="${record.oreOrdinarie || 0}" disabled readonly></td>
                        <td><input type="number" step="0.01" class="edit-input num-input" data-field="oreStraordinarie" value="${record.oreStraordinarie || 0}" disabled readonly></td>
                        <td style="text-align:center;">
                            <input type="hidden" data-field="importo" value="${record.importo || 0}">
                            <input type="hidden" data-field="litri" value="${record.litri || 0}">
                            <input type="hidden" data-field="note" value="${(record.note || '').replace(/"/g, '&quot;')}">
                            <input type="checkbox" data-field="isMagazzino" ${isMagazzino ? 'checked' : ''} style="display:none;" onchange="onDoubleShiftToggle(this)">
                            
                            <div style="display:flex; gap:6px; justify-content:center; align-items:center;">
                                <button class="btn-edit" onclick="toggleRowEdit(this)">✏️ Mod.</button>
                                <button class="btn-dettagli" 
                                    style="${(isMagazzino || parseFloat(record.importo || 0) > 0 || parseFloat(record.litri || 0) > 0 || (record.note && record.note.trim() !== '')) ? 'background-color: #dcfce3; color: #166534; border-color: #86efac;' : ''}" 
                                    onclick="openDettagli(this)">🔍 Dati</button>
                            </div>
                        </td>
                    `;

                    tbody.appendChild(tr);

                    // Accumula totali
                    totalOre += parseFloat(record.oreTotali) || 0.0;
                    totalOrd += parseFloat(record.oreOrdinarie) || 0.0;
                    totalExtra += parseFloat(record.oreStraordinarie) || 0.0;
                    totalDeltaKm += parseFloat(record.kmDelta) || 0.0;
                    totalImporto += parseFloat(record.importo) || 0.0;
                    totalLitri += parseFloat(record.litri) || 0.0;
                }
            });

            // Mostra footer e popola totali
            document.getElementById('tableFoot').style.display = 'table-footer-group';
            const tfootSpazioOre = document.getElementById('tfootSpazioOre');
            if (tfootSpazioOre) {
                tfootSpazioOre.colSpan = forceFourCols ? 4 : 2;
            }
            document.getElementById('totDeltaKm').innerText = totalDeltaKm.toFixed(2);
            document.getElementById('totOre').innerText = totalOre.toFixed(2);
            document.getElementById('totOrd').innerText = totalOrd.toFixed(2);
            document.getElementById('totExtra').innerText = totalExtra.toFixed(2);

            // Popola summary cards
            document.getElementById('sumHours').innerText = totalOre.toFixed(2);
            document.getElementById('sumOrdHours').innerText = totalOrd.toFixed(2);
            document.getElementById('sumExtraHours').innerText = totalExtra.toFixed(2);
            document.getElementById('sumKm').innerText = totalDeltaKm.toFixed(2);
            document.getElementById('sumImporto').innerText = `€ ${totalImporto.toFixed(2)}`;
        }"""

pattern = re.compile(r"        // Genera tutti i giorni del mese selezionato\s*function renderCalendar\(presenzeMap\) \{.*?\n        }\n\n        // Gestione cambio flag orario sdoppiato magazzino", re.DOTALL)
content = pattern.sub(new_render_calendar + "\n\n        // Gestione cambio flag orario sdoppiato magazzino", content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Part 4 injected.")
