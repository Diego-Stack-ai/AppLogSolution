import re

file_path = r"g:\Il mio Drive\App\AppLogSolutionsWeb\frontend\presenze.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# JS global state injection
if "let currentViewMode =" not in content:
    state_vars = """
        let currentUnsub = null;
        let selectedEmployee = null;
        let selectedMonth = "";
        let currentPresenzeData = {};
        
        let currentViewMode = 'mese'; // 'giorno', 'settimana', 'mese'
        let currentSubFilter = null; // id of day or week
"""
    content = re.sub(
        r"let currentUnsub = null;\s*let selectedEmployee = null;\s*let selectedMonth = \"\";\s*let currentPresenzeData = \{\};",
        state_vars,
        content
    )

# Replace onFilterChange
old_filter = r"""            if (!empId || !month) {
                document.getElementById('tableBody').innerHTML = `
                    <tr>
                        <td colspan="17" style="text-align:center; padding: 32px; color: var(--text-muted);">
                            Seleziona un dipendente e un mese per visualizzare il registro delle presenze.
                        </td>
                    </tr>
                `;
                document.getElementById('tableFoot').style.display = 'none';
                resetSummary();
                return;
            }

            selectedEmployee = window.appData.lista_autisti.find(e => e.id === empId);
            selectedMonth = month;

            // Avvia la sottoscrizione Firestore in tempo reale
            const q = query(
                collection(db, "presenze"),
                where("autistaId", "==", empId),
                where("mese", "==", month)
            );"""

new_filter = r"""            if (!empId || !month) {
                document.getElementById('viewModeSection').style.display = 'none';
                document.getElementById('tableBody').innerHTML = `
                    <tr>
                        <td colspan="17" style="text-align:center; padding: 32px; color: var(--text-muted);">
                            Seleziona un dipendente e un mese per visualizzare il registro delle presenze.
                        </td>
                    </tr>
                `;
                document.getElementById('tableFoot').style.display = 'none';
                resetSummary();
                return;
            }

            if (empId === 'tutti') {
                selectedEmployee = { id: 'tutti', nome: 'Tutti i dipendenti', ruolo: 'tutti' };
                document.getElementById('viewModeSection').style.display = 'block';
            } else {
                selectedEmployee = window.appData.lista_autisti.find(e => e.id === empId);
                // Can still show view mode if we want, or hide it. Let's show it so they can filter.
                document.getElementById('viewModeSection').style.display = 'block';
            }
            selectedMonth = month;
            
            renderSubFilters();

            // Avvia la sottoscrizione Firestore in tempo reale
            let q;
            if (empId === 'tutti') {
                q = query(
                    collection(db, "presenze"),
                    where("mese", "==", month)
                );
            } else {
                q = query(
                    collection(db, "presenze"),
                    where("autistaId", "==", empId),
                    where("mese", "==", month)
                );
            }
"""
content = content.replace(old_filter, new_filter)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Part 2 injected.")
