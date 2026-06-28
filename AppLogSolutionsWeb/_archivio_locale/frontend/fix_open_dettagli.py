import re

file_path = r"g:\Il mio Drive\App\AppLogSolutionsWeb\frontend\presenze.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_func = r"""        window.openDettagli = function(btn) {
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
        };"""

new_func = r"""        window.openDettagli = function(btn) {
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
                alert("Si è verificato un errore: " + error.message);
            }
        };"""

if old_func in content:
    content = content.replace(old_func, new_func)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Added try-catch to openDettagli!")
else:
    print("Could not find openDettagli function to replace!")
