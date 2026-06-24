import re

file_path = r"g:\Il mio Drive\App\AppLogSolutionsWeb\frontend\presenze.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

def inject_autista_logic(func_text):
    old_isAdmin = "const isAdmin = selectedEmployee.ruolo === 'amministratore' || selectedEmployee.ruolo === 'impiegata';"
    new_isAdmin = """
            let rowAutista = selectedEmployee;
            if (selectedEmployee && selectedEmployee.id === 'tutti') {
                const aId = tr.dataset.autistaId;
                rowAutista = window.appData.lista_autisti.find(a => a.id === aId) || {};
            }
            const isAdmin = rowAutista.ruolo === 'amministratore' || rowAutista.ruolo === 'impiegata';
"""
    # Replace standard
    t1 = func_text.replace(old_isAdmin, new_isAdmin)
    
    # Also replace isDiego check in recalculateRowHours
    old_isDiego = "const isDiego = selectedEmployee.nome.toLowerCase().includes('diego boschetto') || selectedEmployee.nome.toLowerCase().includes('boschetto diego');"
    new_isDiego = "const isDiego = rowAutista && rowAutista.nome ? (rowAutista.nome.toLowerCase().includes('diego boschetto') || rowAutista.nome.toLowerCase().includes('boschetto diego')) : false;"
    t2 = t1.replace(old_isDiego, new_isDiego)
    
    return t2

# Replace in recalculateRowHours
match_recalc = re.search(r"        function recalculateRowHours\(tr\) \{.*?\n        }", content, re.DOTALL)
if match_recalc:
    content = content.replace(match_recalc.group(0), inject_autista_logic(match_recalc.group(0)))

# Replace in toggleRowEdit
match_toggle = re.search(r"        window\.toggleRowEdit = async function\(btn\) \{.*?\n        };", content, re.DOTALL)
if match_toggle:
    t = match_toggle.group(0)
    # Also, we must change `const defaultDoubleShift = isAdmin;` to use the injected isAdmin.
    t = inject_autista_logic(t)
    
    # In toggleRowEdit, tableHeadTr is updated. If 'tutti', we must force four columns regardless of isAdmin.
    # Wait, we shouldn't update tableHeadTr on row edit! The header is global!
    # Let's just remove the header updating logic inside toggleRowEdit and recalculateRowHours since it shouldn't change when a row is edited.
    # It causes bugs if they edit a row when 'Tutti' is selected!
    header_update_pattern = re.compile(r"            const tableHeadTr = document\.getElementById\('tableHeadTr'\);\s*let headerHtml = `.*?if \(tableHeadTr\) tableHeadTr\.innerHTML = headerHtml;", re.DOTALL)
    t = header_update_pattern.sub("", t)
    
    content = content.replace(match_toggle.group(0), t)

# Also remove header update from recalculateRowHours
match_recalc2 = re.search(r"        function recalculateRowHours\(tr\) \{.*?\n        }", content, re.DOTALL)
if match_recalc2:
    t = match_recalc2.group(0)
    header_update_pattern2 = re.compile(r"            const tableHeadTr = document\.getElementById\('tableHeadTr'\);\s*let headerHtml = `.*?if \(tableHeadTr\) tableHeadTr\.innerHTML = headerHtml;", re.DOTALL)
    t = header_update_pattern2.sub("", t)
    content = content.replace(match_recalc2.group(0), t)

# Replace in openDettagli
match_open = re.search(r"        window\.openDettagli = function\(btn\) \{.*?\n        };", content, re.DOTALL)
if match_open:
    t = match_open.group(0)
    old_isAdmin_open = "const isAdmin = selectedEmployee && (selectedEmployee.ruolo === 'amministratore' || selectedEmployee.ruolo === 'impiegata');"
    new_isAdmin_open = """
                let rowAutista = selectedEmployee;
                if (selectedEmployee && selectedEmployee.id === 'tutti') {
                    const aId = tr.dataset.autistaId;
                    rowAutista = window.appData.lista_autisti.find(a => a.id === aId) || {};
                }
                const isAdmin = rowAutista && (rowAutista.ruolo === 'amministratore' || rowAutista.ruolo === 'impiegata');
"""
    t = t.replace(old_isAdmin_open, new_isAdmin_open)
    content = content.replace(match_open.group(0), t)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Part 5 injected.")
