import re

file_path = r"g:\Il mio Drive\App\AppLogSolutionsWeb\frontend\presenze.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add CSS for new buttons
css_to_add = """
        .view-mode-container {
            display: flex;
            gap: 10px;
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid #e2e8f0;
        }
        .view-mode-btn {
            padding: 8px 16px;
            background: white;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            color: #475569;
            transition: all 0.2s;
        }
        .view-mode-btn.active {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }
        .sub-filter-container {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            margin-top: 12px;
        }
        .sub-filter-btn {
            padding: 6px 12px;
            background: white;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            color: #475569;
        }
        .sub-filter-btn:hover {
            background: #f1f5f9;
        }
        .sub-filter-btn.active {
            background: #334155;
            color: white;
            border-color: #334155;
        }
        .sub-filter-btn.weekend {
            background: #fef08a; /* giallino */
            color: #854d0e;
            border-color: #fde047;
        }
        .sub-filter-btn.weekend.active {
            background: #eab308;
            color: white;
            border-color: #ca8a04;
        }
        .employee-separator {
            background: #f8fafc;
            border-top: 2px solid #cbd5e1;
            border-bottom: 2px solid #e2e8f0;
        }
        .employee-separator td {
            padding: 12px;
            font-weight: bold;
            color: #1e293b;
            text-transform: uppercase;
            font-size: 14px;
        }
"""
if ".view-mode-container" not in content:
    content = content.replace("</style>", css_to_add + "\n</style>")

# 2. Add UI containers below filters-container
filters_html = """
            <div class="filters-container">
                <div class="filter-item">
                    <label for="selectEmployee">Dipendente</label>
                    <select id="selectEmployee">
                        <option value="">Caricamento dipendenti...</option>
                    </select>
                </div>
                <div class="filter-item">
                    <label for="inputMonth">Mese di Riferimento</label>
                    <input type="month" id="inputMonth">
                </div>
            </div>
"""
new_filters_html = filters_html.strip() + """
            <div id="viewModeSection" style="display:none;">
                <div class="view-mode-container">
                    <button class="view-mode-btn" data-mode="giorno" onclick="setViewMode('giorno')">Giorno</button>
                    <button class="view-mode-btn" data-mode="settimana" onclick="setViewMode('settimana')">Settimana</button>
                    <button class="view-mode-btn active" data-mode="mese" onclick="setViewMode('mese')">Mese</button>
                </div>
                <div id="subFilterContainer" class="sub-filter-container"></div>
            </div>
"""
if 'id="viewModeSection"' not in content:
    content = content.replace(filters_html, new_filters_html)

# Add Option 'tutti' inside JS function renderAutistiDropdown
old_render_autisti = """            select.innerHTML = '<option value="">-- Seleziona Dipendente --</option>';"""
new_render_autisti = """            select.innerHTML = '<option value="">-- Seleziona Dipendente --</option>\\n<option value="tutti">-- Tutti i dipendenti --</option>';"""
if '<option value="tutti">' not in content:
    content = content.replace(old_render_autisti, new_render_autisti)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Part 1 injected.")
