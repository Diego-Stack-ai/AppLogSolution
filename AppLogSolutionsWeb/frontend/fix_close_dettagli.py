import re

file_path = r"g:\Il mio Drive\App\AppLogSolutionsWeb\frontend\presenze.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Restore openDettagli without annoying alerts
old_open = r"""        window.openDettagli = function(btn) {
            alert("DEBUG 1: Funzione openDettagli chiamata con successo!");
            try {
                const tr = btn.closest('tr');
                if (!tr) throw new Error("Riga TR non trovata");
                
                currentRowForModal = tr;
                
                const isMagazzino = tr.querySelector('[data-field="isMagazzino"]') ? tr.querySelector('[data-field="isMagazzino"]').checked : false;
                const importo = tr.querySelector('[data-field="importo"]') ? tr.querySelector('[data-field="importo"]').value : 0;
                const litri = tr.querySelector('[data-field="litri"]') ? tr.querySelector('[data-field="litri"]').value : 0;
                const note = tr.querySelector('[data-field="note"]') ? tr.querySelector('[data-field="note"]').value : '';

                // Check if row is in edit mode (btn-edit has btn-save class or is disabled)
                const btnEdit = tr.querySelector('.btn-edit');
                const isEditing = btnEdit ? btnEdit.innerText.includes('Salva') : false;

                const chkMagazzino = document.getElementById('modalMagazzino');
                const inImporto = document.getElementById('modalImporto');
                const inLitri = document.getElementById('modalLitri');
                const inNote = document.getElementById('modalNote');

                if (!chkMagazzino || !inImporto || !inLitri || !inNote) throw new Error("Campi modale non trovati");

                chkMagazzino.checked = isMagazzino;
                inImporto.value = importo;
                inLitri.value = litri;
                inNote.value = note;

                const isAdmin = selectedEmployee && (selectedEmployee.ruolo === 'amministratore' || selectedEmployee.ruolo === 'impiegata');
                
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
                if (btnSave) {
                    btnSave.style.display = isEditing ? 'block' : 'none';
                }

                const titleEl = document.getElementById('modalTitle');
                if (titleEl) titleEl.innerText = 'Dettagli ' + (tr.dataset.date || '');
                
                const mod = document.getElementById('dettagliModal');
                if (mod) {
                    alert("DEBUG 2: Trovato dettagliModal nel DOM! Imposto display a flex.");
                    mod.style.display = 'flex';
                    mod.style.visibility = 'visible';
                    mod.style.opacity = '1';
                    alert("DEBUG 3: display impostato a " + mod.style.display);
                }
                else throw new Error("Overlay modale non trovato");
            } catch (error) {
                console.error("Errore openDettagli:", error);
                alert("Si è verificato un errore: " + error.message);
            }
        };"""

new_open = r"""        window.openDettagli = function(btn) {
            try {
                const tr = btn.closest('tr');
                if (!tr) throw new Error("Riga TR non trovata");
                
                currentRowForModal = tr;
                
                const isMagazzino = tr.querySelector('[data-field="isMagazzino"]') ? tr.querySelector('[data-field="isMagazzino"]').checked : false;
                const importo = tr.querySelector('[data-field="importo"]') ? tr.querySelector('[data-field="importo"]').value : 0;
                const litri = tr.querySelector('[data-field="litri"]') ? tr.querySelector('[data-field="litri"]').value : 0;
                const note = tr.querySelector('[data-field="note"]') ? tr.querySelector('[data-field="note"]').value : '';

                // Check if row is in edit mode (btn-edit has btn-save class or is disabled)
                const btnEdit = tr.querySelector('.btn-edit');
                const isEditing = btnEdit ? btnEdit.innerText.includes('Salva') : false;

                const chkMagazzino = document.getElementById('modalMagazzino');
                const inImporto = document.getElementById('modalImporto');
                const inLitri = document.getElementById('modalLitri');
                const inNote = document.getElementById('modalNote');

                if (!chkMagazzino || !inImporto || !inLitri || !inNote) throw new Error("Campi modale non trovati");

                chkMagazzino.checked = isMagazzino;
                inImporto.value = importo;
                inLitri.value = litri;
                inNote.value = note;

                const isAdmin = selectedEmployee && (selectedEmployee.ruolo === 'amministratore' || selectedEmployee.ruolo === 'impiegata');
                
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
                if (btnSave) {
                    btnSave.style.display = isEditing ? 'block' : 'none';
                }

                const titleEl = document.getElementById('modalTitle');
                if (titleEl) titleEl.innerText = 'Dettagli ' + (tr.dataset.date || '');
                
                const mod = document.getElementById('dettagliModal');
                if (mod) mod.style.display = 'flex';
                else throw new Error("Overlay modale non trovato");
            } catch (error) {
                console.error("Errore openDettagli:", error);
                alert("Errore in apertura: " + error.message);
            }
        };"""

if old_open in content:
    content = content.replace(old_open, new_open)
else:
    print("Could not find old_open")

# Make closeDettagli robust with try-catch
old_close = r"""        window.closeDettagli = function(save) {
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
            document.getElementById('dettagliModal').style.display = 'none';
            currentRowForModal = null;
        };"""

new_close = r"""        window.closeDettagli = function(save) {
            try {
                if (save && currentRowForModal) {
                    const btnEdit = currentRowForModal.querySelector('.btn-edit');
                    const isEditing = btnEdit ? btnEdit.innerText.includes('Salva') : false;
                    if (isEditing) {
                        const hiddenMag = currentRowForModal.querySelector('[data-field="isMagazzino"]');
                        const hiddenImp = currentRowForModal.querySelector('[data-field="importo"]');
                        const hiddenLit = currentRowForModal.querySelector('[data-field="litri"]');
                        const hiddenNot = currentRowForModal.querySelector('[data-field="note"]');

                        const chkMag = document.getElementById('modalMagazzino');
                        const newMag = chkMag ? chkMag.checked : false;
                        
                        if (hiddenMag && hiddenMag.checked !== newMag) {
                            hiddenMag.checked = newMag;
                            // trigger toggle visual
                            if (typeof onDoubleShiftToggle === 'function') {
                                onDoubleShiftToggle(hiddenMag);
                            }
                        }

                        if (hiddenImp) {
                            const modImp = document.getElementById('modalImporto');
                            hiddenImp.value = modImp ? modImp.value : 0;
                        }
                        if (hiddenLit) {
                            const modLit = document.getElementById('modalLitri');
                            hiddenLit.value = modLit ? modLit.value : 0;
                        }
                        if (hiddenNot) {
                            const modNot = document.getElementById('modalNote');
                            hiddenNot.value = modNot ? modNot.value : '';
                        }
                        
                        // Update button color immediately
                        const hasData = newMag || parseFloat(hiddenImp ? hiddenImp.value : 0) > 0 || parseFloat(hiddenLit ? hiddenLit.value : 0) > 0 || (hiddenNot && hiddenNot.value.trim() !== '');
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
                const mod = document.getElementById('dettagliModal');
                if (mod) mod.style.display = 'none';
                currentRowForModal = null;
            } catch (error) {
                console.error("Errore in closeDettagli:", error);
                alert("Errore in chiusura: " + error.message);
                
                // Fallback attempt to hide modal
                const mod = document.getElementById('dettagliModal');
                if (mod) mod.style.display = 'none';
            }
        };"""

if old_close in content:
    content = content.replace(old_close, new_close)
else:
    print("Could not find old_close")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Applied fix!")
