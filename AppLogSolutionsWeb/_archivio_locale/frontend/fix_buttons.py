import re

file_path = r"g:\Il mio Drive\App\AppLogSolutionsWeb\frontend\presenze.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update the button html in renderCalendar
old_td = r"""                    <td style="text-align:center; white-space:nowrap;">
                        <input type="hidden" data-field="importo" value="${record.importo || 0}">
                        <input type="hidden" data-field="litri" value="${record.litri || 0}">
                        <input type="hidden" data-field="note" value="${record.note || ''}">
                        <input type="checkbox" data-field="isMagazzino" ${isMagazzino ? 'checked' : ''} style="display:none;" onchange="onDoubleShiftToggle(this)">
                        
                        <button class="btn-edit" onclick="toggleRowEdit(this)">✏️ Mod.</button>
                        <button class="btn-dettagli" onclick="openDettagli(this)">🔍 Det.</button>
                    </td>"""

new_td = r"""                    <td style="text-align:center;">
                        <input type="hidden" data-field="importo" value="${record.importo || 0}">
                        <input type="hidden" data-field="litri" value="${record.litri || 0}">
                        <input type="hidden" data-field="note" value="${record.note || ''}">
                        <input type="checkbox" data-field="isMagazzino" ${isMagazzino ? 'checked' : ''} style="display:none;" onchange="onDoubleShiftToggle(this)">
                        
                        <div style="display:flex; gap:6px; justify-content:center; align-items:center;">
                            <button class="btn-edit" onclick="toggleRowEdit(this)">✏️ Mod.</button>
                            <button class="btn-dettagli" 
                                style="${(isMagazzino || parseFloat(record.importo || 0) > 0 || parseFloat(record.litri || 0) > 0 || (record.note && record.note.trim() !== '')) ? 'background-color: #dcfce3; color: #166534; border-color: #86efac;' : ''}" 
                                onclick="openDettagli(this)">🔍 Dati</button>
                        </div>
                    </td>"""
content = content.replace(old_td, new_td)

# 2. Update closeDettagli to update the button color dynamically
old_close = r"""                    if (hiddenMag.checked !== newMag) {
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
            document.getElementById('dettagliModal').style.display = 'none';"""

new_close = r"""                    if (hiddenMag.checked !== newMag) {
                        hiddenMag.checked = newMag;
                        // trigger toggle visual
                        if (typeof onDoubleShiftToggle === 'function') {
                            onDoubleShiftToggle(hiddenMag);
                        }
                    }

                    hiddenImp.value = document.getElementById('modalImporto').value;
                    hiddenLit.value = document.getElementById('modalLitri').value;
                    hiddenNot.value = document.getElementById('modalNote').value;
                    
                    // Update button color immediately
                    const hasData = hiddenMag.checked || parseFloat(hiddenImp.value || 0) > 0 || parseFloat(hiddenLit.value || 0) > 0 || hiddenNot.value.trim() !== '';
                    const btnDet = currentRowForModal.querySelector('.btn-dettagli');
                    if (btnDet) {
                        if (hasData) {
                            btnDet.style.backgroundColor = '#dcfce3';
                            btnDet.style.color = '#166534';
                            btnDet.style.borderColor = '#86efac';
                        } else {
                            btnDet.style.backgroundColor = '';
                            btnDet.style.color = '';
                            btnDet.style.borderColor = '';
                        }
                    }
                }
            }
            document.getElementById('dettagliModal').style.display = 'none';"""
content = content.replace(old_close, new_close)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated buttons successfully!")
