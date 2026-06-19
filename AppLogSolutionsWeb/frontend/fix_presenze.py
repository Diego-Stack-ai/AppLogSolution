import re

with open(r"g:\Il mio Drive\App\AppLogSolutionsWeb\frontend\presenze.html", "r", encoding="utf-8") as f:
    content = f.read()

# 2. Update renderCalendar
old_render = r"""            const isDiego = selectedEmployee.nome.toLowerCase().includes('diego boschetto') || selectedEmployee.nome.toLowerCase().includes('boschetto diego');
            const isIona = selectedEmployee.nome.toLowerCase().includes('jona') || selectedEmployee.nome.toLowerCase().includes('iona');
            const defaultDoubleShift = isDiego || isIona || (selectedEmployee.tipoTurno === 'giornata');"""

new_render = r"""            const isAdmin = selectedEmployee.ruolo === 'amministratore' || selectedEmployee.ruolo === 'impiegata';
            const defaultDoubleShift = isAdmin;

            const tableHeadTr = document.getElementById('tableHeadTr');
            let headerHtml = `
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
            `;
            if (tableHeadTr) tableHeadTr.innerHTML = headerHtml;
"""
content = content.replace(old_render, new_render)

# 3. Update the HTML row template in renderCalendar
old_tr = r"""                    <td><input type="text" class="edit-input time-input" data-field="oraInizioM" value="${record.oraInizioM || ''}" disabled placeholder="00:00" onchange="onTimeChange(this)"></td>
                    <td><input type="text" class="edit-input time-input" data-field="oraFineM" value="${record.oraFineM || ''}" disabled placeholder="00:00" onchange="onTimeChange(this)"></td>
                    <td><input type="text" class="edit-input time-input" data-field="oraInizioP" value="${record.oraInizioP || ''}" disabled placeholder="00:00" ${isDoubleShift ? '' : 'style="opacity:0.3;"'} onchange="onTimeChange(this)"></td>
                    <td><input type="text" class="edit-input time-input" data-field="oraFineP" value="${record.oraFineP || ''}" disabled placeholder="00:00" ${isDoubleShift ? '' : 'style="opacity:0.3;"'} onchange="onTimeChange(this)"></td>"""

new_tr = r"""                    ${isAdmin ? `
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
                    `}"""
content = content.replace(old_tr, new_tr)

# 4. Update onDoubleShiftToggle
old_toggle = r"""        window.onDoubleShiftToggle = function(chk) {
            const tr = chk.closest('tr');
            const isChecked = chk.checked;
            const oraInizioP = tr.querySelector('[data-field="oraInizioP"]');
            const oraFineP = tr.querySelector('[data-field="oraFineP"]');

            if (isChecked) {
                oraInizioP.style.opacity = "1";
                oraFineP.style.opacity = "1";
            } else {
                oraInizioP.value = "";
                oraFineP.value = "";
                oraInizioP.style.opacity = "0.3";
                oraFineP.style.opacity = "0.3";
            }
            recalculateRowHours(tr);
        };"""

new_toggle = r"""        window.onDoubleShiftToggle = function(chk) {
            const tr = chk.closest('tr');
            const isChecked = chk.checked;
            const oraInizioP = tr.querySelector('[data-field="oraInizioP"]');
            const oraFineP = tr.querySelector('[data-field="oraFineP"]');

            const isAdmin = selectedEmployee.ruolo === 'amministratore' || selectedEmployee.ruolo === 'impiegata';

            if (isAdmin) {
                oraInizioP.style.opacity = isChecked ? "1" : "0.3";
                oraFineP.style.opacity = isChecked ? "1" : "0.3";
            } else {
                if (isChecked) {
                    oraInizioP.style.display = "block";
                    oraFineP.style.display = "block";
                } else {
                    oraInizioP.value = "";
                    oraFineP.value = "";
                    oraInizioP.style.display = "none";
                    oraFineP.style.display = "none";
                }
            }
            recalculateRowHours(tr);
        };"""
content = content.replace(old_toggle, new_toggle)

# 5. Update recalculateRowHours
old_recalc = r"""            const isDiego = selectedEmployee.nome.toLowerCase().includes('diego boschetto') || selectedEmployee.nome.toLowerCase().includes('boschetto diego');
            const isIona = selectedEmployee.nome.toLowerCase().includes('jona') || selectedEmployee.nome.toLowerCase().includes('iona');
            const defaultDoubleShift = isDiego || isIona || (selectedEmployee.tipoTurno === 'giornata');"""

new_recalc = r"""            const isAdmin = selectedEmployee.ruolo === 'amministratore' || selectedEmployee.ruolo === 'impiegata';
            const defaultDoubleShift = isAdmin;"""
content = content.replace(old_recalc, new_recalc)

# And fix standardHours in recalculateRowHours
old_std = r"""            const standardHours = isDiego ? 8.0 : 8.5;"""
new_std = r"""            const isDiego = selectedEmployee.nome.toLowerCase().includes('diego boschetto') || selectedEmployee.nome.toLowerCase().includes('boschetto diego');
            const standardHours = isDiego ? 8.0 : 8.5;"""
content = content.replace(old_std, new_std)

# 6. Update toggleRowEdit
old_edit = r"""            const isDiego = selectedEmployee.nome.toLowerCase().includes('diego boschetto') || selectedEmployee.nome.toLowerCase().includes('boschetto diego');
            const isIona = selectedEmployee.nome.toLowerCase().includes('jona') || selectedEmployee.nome.toLowerCase().includes('iona');
            const defaultDoubleShift = isDiego || isIona || (selectedEmployee.tipoTurno === 'giornata');"""
content = content.replace(old_edit, new_recalc)

# 7. Also make sure the tfoot spans the correct number of columns
old_foot = r"""            // Mostra footer e popola totali
            document.getElementById('tableFoot').style.display = 'table-footer-group';"""

new_foot = r"""            // Mostra footer e popola totali
            document.getElementById('tableFoot').style.display = 'table-footer-group';
            const tfootTotals = document.querySelector('.tfoot-totals');
            if (tfootTotals) {
                if (isAdmin) {
                    tfootTotals.children[6].colSpan = 4; // Spazio sotto le 4 colonne ore
                } else {
                    tfootTotals.children[6].colSpan = 2; // Spazio sotto le 2 colonne ore
                }
            }"""
content = content.replace(old_foot, new_foot)

with open(r"g:\Il mio Drive\App\AppLogSolutionsWeb\frontend\presenze.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Fix applied successfully!")
