import re

file_path = r"g:\Il mio Drive\App\AppLogSolutionsWeb\frontend\presenze.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Modal CSS
modal_css = """
        /* MODAL STYLES */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(15, 23, 42, 0.6);
            z-index: 1000;
            backdrop-filter: blur(4px);
            align-items: center;
            justify-content: center;
        }
        .modal-box {
            background: white;
            border-radius: 16px;
            width: 90%;
            max-width: 400px;
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            animation: modalFadeIn 0.3s ease-out;
        }
        @keyframes modalFadeIn {
            from { opacity: 0; transform: translateY(20px) scale(0.95); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        .modal-header {
            padding: 16px 20px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #f8fafc;
        }
        .modal-header h3 {
            margin: 0; font-size: 16px; color: #1e293b;
        }
        .modal-close {
            background: none; border: none; font-size: 20px; color: #64748b; cursor: pointer;
        }
        .modal-body {
            padding: 20px;
            display: flex; flex-direction: column; gap: 16px;
        }
        .modal-field {
            display: flex; flex-direction: column; gap: 6px;
        }
        .modal-field label {
            font-size: 12px; font-weight: 600; color: #475569;
        }
        .modal-field input[type="number"], .modal-field input[type="text"] {
            padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px;
        }
        .modal-field.checkbox-field {
            flex-direction: row; align-items: center; gap: 10px;
        }
        .modal-footer {
            padding: 16px 20px; border-top: 1px solid #e2e8f0; display: flex; justify-content: flex-end; gap: 10px; background: #f8fafc;
        }
        .btn-modal-cancel {
            padding: 8px 16px; background: white; border: 1px solid #cbd5e1; border-radius: 8px; cursor: pointer; font-weight: 500;
        }
        .btn-modal-save {
            padding: 8px 16px; background: var(--primary); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 500;
        }
        .btn-dettagli {
            padding: 4px 8px; background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; border-radius: 6px; cursor: pointer; font-size: 11px; margin-left: 4px;
        }
        .btn-dettagli:hover { background: #e2e8f0; }
"""
if "/* MODAL STYLES */" not in content:
    content = content.replace("</style>", modal_css + "</style>")

# 2. Add Modal HTML before </body>
modal_html = """
    <!-- DETTAGLI MODAL -->
    <div id="dettagliModal" class="modal-overlay">
        <div class="modal-box">
            <div class="modal-header">
                <h3 id="modalTitle">Dettagli Riga</h3>
                <button class="modal-close" onclick="closeDettagli(false)">×</button>
            </div>
            <div class="modal-body">
                <div class="modal-field checkbox-field">
                    <input type="checkbox" id="modalMagazzino">
                    <label for="modalMagazzino">Magazzino Sdoppiato (Doppio Turno)</label>
                </div>
                <div class="modal-field">
                    <label>Importo (€)</label>
                    <input type="number" id="modalImporto" step="0.01">
                </div>
                <div class="modal-field">
                    <label>Litri</label>
                    <input type="number" id="modalLitri" step="0.01">
                </div>
                <div class="modal-field">
                    <label>Note</label>
                    <input type="text" id="modalNote">
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn-modal-cancel" onclick="closeDettagli(false)">Annulla</button>
                <button class="btn-modal-save" onclick="closeDettagli(true)">Applica</button>
            </div>
        </div>
    </div>
"""
if "<!-- DETTAGLI MODAL -->" not in content:
    content = content.replace("</body>", modal_html + "\n</body>")

# 3. Update table headers in renderCalendar
old_header = r"""            let headerHtml = `
                <th>Data</th>
                <th style="text-align:center;">Magazzino<br>Sdoppiato</th>
                <th>Cliente</th>
                <th style="text-align:right;">Km<br>Part.</th>
                <th style="text-align:right;">Km<br>Arr.</th>
                <th style="text-align:right;">Delta<br>Km</th>
            `;
            if (isAdmin) {
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
                <th style="text-align:right;">Importo</th>
                <th style="text-align:right;">Litri</th>
                <th>Note</th>
                <th style="text-align:center;">Azione</th>
            `;"""

new_header = r"""            let headerHtml = `
                <th>Data</th>
                <th>Cliente</th>
                <th style="text-align:right;">Km<br>Part.</th>
                <th style="text-align:right;">Km<br>Arr.</th>
                <th style="text-align:right;">Delta<br>Km</th>
            `;
            if (isAdmin) {
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
            `;"""

old_header_re = re.compile(r"let headerHtml = `.*?<th>Data</th>.*?<th style=\"text-align:center;\">Magazzino<br>Sdoppiato</th>.*?<th style=\"text-align:center;\">Azione</th>\s*`;", re.DOTALL)
content = old_header_re.sub(new_header.strip(), content)

# 4. Update table row template in renderCalendar
old_tr_re = re.compile(r"                    <td><strong>\$\{dayName\}</strong><br><span style=\"font-size: 0\.8em; color: #6b7280;\">\$\{displayDate\}</span></td>.*?<button class=\"btn-edit\" onclick=\"toggleRowEdit\(this\)\">.*?Modifica</button>\s*</td>", re.DOTALL)

new_tr = r"""                    <td><strong>${dayName}</strong><br><span style="font-size: 0.8em; color: #6b7280;">${displayDate}</span></td>
                    <td><input type="text" class="edit-input" data-field="cliente" value="${record.cliente || ''}" disabled></td>
                    <td><input type="number" class="edit-input num-input" data-field="kmPartenza" value="${record.kmPartenza || 0}" disabled onchange="onKmChange(this)"></td>
                    <td><input type="number" class="edit-input num-input" data-field="kmArrivo" value="${record.kmArrivo || 0}" disabled onchange="onKmChange(this)"></td>
                    <td><input type="number" class="edit-input num-input" data-field="kmDelta" value="${record.kmDelta || 0}" disabled readonly></td>
                    ${isAdmin ? `
                        <td><input type="text" class="edit-input time-input" data-field="oraInizioM" value="${record.oraInizioM || ''}" disabled placeholder="00:00" onchange="onTimeChange(this)"></td>
                        <td><input type="text" class="edit-input time-input" data-field="oraFineM" value="${record.oraFineM || ''}" disabled placeholder="00:00" onchange="onTimeChange(this)"></td>
                        <td><input type="text" class="edit-input time-input" data-field="oraInizioP" value="${record.oraInizioP || ''}" disabled placeholder="00:00" onchange="onTimeChange(this)"></td>
                        <td><input type="text" class="edit-input time-input" data-field="oraFineP" value="${record.oraFineP || ''}" disabled placeholder="00:00" onchange="onTimeChange(this)"></td>
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
                    <td style="text-align:center; white-space:nowrap;">
                        <input type="hidden" data-field="importo" value="${record.importo || 0}">
                        <input type="hidden" data-field="litri" value="${record.litri || 0}">
                        <input type="hidden" data-field="note" value="${record.note || ''}">
                        <input type="checkbox" data-field="isMagazzino" ${isMagazzino ? 'checked' : ''} style="display:none;" onchange="onDoubleShiftToggle(this)">
                        
                        <button class="btn-edit" onclick="toggleRowEdit(this)">✏️ Mod.</button>
                        <button class="btn-dettagli" onclick="openDettagli(this)">🔍 Det.</button>
                    </td>"""

content = old_tr_re.sub(new_tr.strip(), content)

# 5. Fix tfoot colspan
old_static_tfoot = r"""                    <tfoot id="tableFoot" style="display:none;">
                        <tr class="tfoot-totals">
                            <td colspan="5" style="text-align:right; font-weight:bold;">Totali:</td>
                            <td id="totDeltaKm" style="text-align:right; font-weight:bold;">0.00</td>
                            <td colspan="4"></td> <!-- Spazio ore -->
                            <td id="totOre" style="text-align:right; font-weight:bold;">0.00</td>
                            <td id="totOrd" style="text-align:right; font-weight:bold;">0.00</td>
                            <td id="totExtra" style="text-align:right; font-weight:bold;">0.00</td>
                            <td id="totImporto" style="text-align:right; font-weight:bold;">€ 0.00</td>
                            <td id="totLitri" style="text-align:right; font-weight:bold;">0.00</td>
                            <td colspan="2"></td>
                        </tr>
                    </tfoot>"""

new_static_tfoot = r"""                    <tfoot id="tableFoot" style="display:none;">
                        <tr class="tfoot-totals">
                            <td colspan="4" style="text-align:right; font-weight:bold;">Totali:</td>
                            <td id="totDeltaKm" style="text-align:right; font-weight:bold;">0.00</td>
                            <td colspan="2" id="tfootSpazioOre"></td> <!-- Spazio ore (2 o 4 cols) -->
                            <td id="totOre" style="text-align:right; font-weight:bold;">0.00</td>
                            <td id="totOrd" style="text-align:right; font-weight:bold;">0.00</td>
                            <td id="totExtra" style="text-align:right; font-weight:bold;">0.00</td>
                            <td></td>
                        </tr>
                    </tfoot>"""
content = content.replace(old_static_tfoot, new_static_tfoot)

old_foot_dynamic = r"""            if (tfootTotals) {
                if (isAdmin) {
                    tfootTotals.children[6].colSpan = 4; // Spazio sotto le 4 colonne ore
                } else {
                    tfootTotals.children[6].colSpan = 2; // Spazio sotto le 2 colonne ore
                }
            }
            document.getElementById('totDeltaKm').innerText = totalDeltaKm.toFixed(2);
            document.getElementById('totOre').innerText = totalOre.toFixed(2);
            document.getElementById('totOrd').innerText = totalOrd.toFixed(2);
            document.getElementById('totExtra').innerText = totalExtra.toFixed(2);
            document.getElementById('totImporto').innerText = `€ ${totalImporto.toFixed(2)}`;
            document.getElementById('totLitri').innerText = totalLitri.toFixed(2);"""

new_foot_dynamic = r"""            const tfootSpazioOre = document.getElementById('tfootSpazioOre');
            if (tfootSpazioOre) {
                tfootSpazioOre.colSpan = isAdmin ? 4 : 2;
            }
            document.getElementById('totDeltaKm').innerText = totalDeltaKm.toFixed(2);
            document.getElementById('totOre').innerText = totalOre.toFixed(2);
            document.getElementById('totOrd').innerText = totalOrd.toFixed(2);
            document.getElementById('totExtra').innerText = totalExtra.toFixed(2);"""
content = content.replace(old_foot_dynamic, new_foot_dynamic)


# 6. JS functions for the modal
js_functions = """
        let currentRowForModal = null;

        window.openDettagli = function(btn) {
            const tr = btn.closest('tr');
            currentRowForModal = tr;
            
            const isMagazzino = tr.querySelector('[data-field="isMagazzino"]').checked;
            const importo = tr.querySelector('[data-field="importo"]').value;
            const litri = tr.querySelector('[data-field="litri"]').value;
            const note = tr.querySelector('[data-field="note"]').value;

            // Check if row is in edit mode (btn-edit has btn-save class or is disabled)
            const isEditing = tr.querySelector('.btn-edit').innerText.includes('Salva');

            const chkMagazzino = document.getElementById('modalMagazzino');
            const inImporto = document.getElementById('modalImporto');
            const inLitri = document.getElementById('modalLitri');
            const inNote = document.getElementById('modalNote');

            chkMagazzino.checked = isMagazzino;
            inImporto.value = importo;
            inLitri.value = litri;
            inNote.value = note;

            const isAdmin = selectedEmployee.ruolo === 'amministratore' || selectedEmployee.ruolo === 'impiegata';
            
            if (isAdmin) {
                chkMagazzino.disabled = true;
            } else {
                chkMagazzino.disabled = !isEditing;
            }

            inImporto.disabled = !isEditing;
            inLitri.disabled = !isEditing;
            inNote.disabled = !isEditing;

            // Nascondi pulsante applica se non stiamo modificando
            const btnSave = document.querySelector('.btn-modal-save');
            if (isEditing) {
                btnSave.style.display = 'block';
            } else {
                btnSave.style.display = 'none';
            }

            document.getElementById('modalTitle').innerText = 'Dettagli ' + tr.dataset.date;
            document.getElementById('dettagliModal').style.display = 'flex';
        };

        window.closeDettagli = function(save) {
            if (save && currentRowForModal) {
                const isEditing = currentRowForModal.querySelector('.btn-edit').innerText.includes('Salva');
                if (isEditing) {
                    const hiddenMag = currentRowForModal.querySelector('[data-field="isMagazzino"]');
                    const hiddenImp = currentRowForModal.querySelector('[data-field="importo"]');
                    const hiddenLit = currentRowForModal.querySelector('[data-field="litri"]');
                    const hiddenNot = currentRowForModal.querySelector('[data-field="note"]');

                    const newMag = document.getElementById('modalMagazzino').checked;
                    
                    if (hiddenMag.checked !== newMag) {
                        hiddenMag.checked = newMag;
                        // trigger toggle visual
                        if (typeof onDoubleShiftToggle === 'function') {
                            onDoubleShiftToggle(hiddenMag);
                        }
                    }

                    hiddenImp.value = document.getElementById('modalImporto').value;
                    hiddenLit.value = document.getElementById('modalLitri').value;
                    hiddenNot.value = document.getElementById('modalNote').value;
                }
            }
            document.getElementById('dettagliModal').style.display = 'none';
            currentRowForModal = null;
        };
"""

if "window.openDettagli =" not in content:
    content = content.replace("// Toggle edit della riga", js_functions + "\n        // Toggle edit della riga")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Applied modal successfully!")
