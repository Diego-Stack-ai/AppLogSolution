import os
import pandas as pd
import json
from datetime import datetime

cartella = r"g:\Il mio Drive\1-PRESENZE 2026"
tutti_i_dati = []

print("--- INIZIO ESTRAZIONE DATI ---")
for file in os.listdir(cartella):
    if file.endswith(".xlsx") and not file.startswith("~$"):
        percorso = os.path.join(cartella, file)
        autista = file.replace(".xlsx", "").strip()
        print(f"Estraggo presenze per: {autista}...")
        
        try:
            excel_file = pd.ExcelFile(percorso)
            for mese in excel_file.sheet_names:
                df = pd.read_excel(percorso, sheet_name=mese)
                
                col_names = [str(c).lower().strip() for c in df.columns]
                
                idx_data = -1
                for i, col in enumerate(col_names):
                    if col == 'data':
                        idx_data = i
                        break
                if idx_data == -1:
                    continue
                
                def get_idx(keywords):
                    for i, col in enumerate(col_names):
                        if any(kw == col for kw in keywords): return i
                    for i, col in enumerate(col_names):
                        if any(kw in col for kw in keywords): return i
                    return -1

                idx_cliente = get_idx(['cliente'])
                idx_kmdelta = get_idx(['delta km'])
                idx_orainizio = get_idx(['ora inizio m', 'ora inizio'])
                idx_orafine = get_idx(['ora fine m', 'ora fine'])
                idx_ore = get_idx(['orario giornaliero', 'ore', 'totale'])
                idx_note = get_idx(['note'])
                
                for index, row in df.iterrows():
                    data_cella = row.iloc[idx_data]
                    if pd.isna(data_cella) or not isinstance(data_cella, datetime):
                        continue
                        
                    def get_val(idx):
                        if idx != -1 and not pd.isna(row.iloc[idx]): return row.iloc[idx]
                        return ""
                        
                    cliente = str(get_val(idx_cliente))
                    km_delta = get_val(idx_kmdelta)
                    ora_in = get_val(idx_orainizio)
                    ora_out = get_val(idx_orafine)
                    ore_totali = get_val(idx_ore)
                    note = str(get_val(idx_note))
                    
                    if hasattr(ora_in, 'strftime'): ora_in = ora_in.strftime('%H:%M')
                    else: ora_in = str(ora_in)
                    
                    if hasattr(ora_out, 'strftime'): ora_out = ora_out.strftime('%H:%M')
                    else: ora_out = str(ora_out)
                    
                    km_val = float(km_delta) if str(km_delta).replace('.','',1).isdigit() else 0
                    
                    if isinstance(ore_totali, (int, float)):
                        ore_val = float(ore_totali)
                    elif isinstance(ore_totali, str):
                        ore_totali_clean = str(ore_totali).replace(',','.').replace(' ','')
                        try:
                            ore_val = float(ore_totali_clean)
                        except:
                            ore_val = 0
                    else:
                        ore_val = 0
                        
                    if hasattr(ore_totali, 'hour'):
                        ore_val = ore_totali.hour + ore_totali.minute / 60.0
                    
                    tutti_i_dati.append({
                        "autista": autista,
                        "mese": mese,
                        "data": data_cella.strftime("%Y-%m-%dT00:00:00.000Z"),
                        "cliente": cliente,
                        "kmDelta": km_val,
                        "oraInizioM": ora_in,
                        "oraFineM": ora_out,
                        "oreTotali": round(ore_val, 2),
                        "note": note
                    })
        except Exception as e:
            print(f"Errore file {file}: {e}")

tutti_i_dati.sort(key=lambda x: (x["autista"], x["data"]))
dati_json_string = json.dumps(tutti_i_dati, ensure_ascii=False)

print(f"Totale record estratti correttamente da tutti i mesi: {len(tutti_i_dati)}")
print("\n--- GENERAZIONE DASHBOARD HTML ---")

html_template = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Presenze Autisti</title>
    <style>
        :root {{ --bg-color: #f3f4f6; --text-color: #1f2937; --card-bg: #ffffff; --primary: #3b82f6; --primary-hover: #2563eb; --weekend-bg: #fee2e2; --weekend-text: #991b1b; --border: #e5e7eb; }}
        body {{ font-family: 'Segoe UI', system-ui, sans-serif; background-color: var(--bg-color); margin: 0; padding: 2rem; display: flex; flex-direction: column; align-items: center; }}
        h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; color: #111827; }}
        .subtitle {{ color: #6b7280; margin-bottom: 2rem; }}
        .container {{ width: 100%; max-width: 1200px; background: var(--card-bg); border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); padding: 2rem; }}
        .controls {{ display: flex; gap: 1rem; margin-bottom: 2rem; align-items: center; flex-wrap: wrap; }}
        .btn-group {{ display: flex; border-radius: 8px; overflow: hidden; border: 1px solid var(--border); }}
        .btn-group button {{ background: #f9fafb; border: none; padding: 0.75rem 1.5rem; cursor: pointer; font-weight: 600; color: #4b5563; border-right: 1px solid var(--border); transition: 0.2s; }}
        .btn-group button:last-child {{ border-right: none; }}
        .btn-group button.active {{ background: var(--primary); color: white; }}
        input[type="date"], input[type="week"], input[type="month"] {{ padding: 0.5rem; border: 1px solid var(--border); border-radius: 6px; font-family: inherit; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; }}
        th {{ background: #f9fafb; padding: 1rem; border-bottom: 2px solid var(--border); color: #374151; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.05em; }}
        td {{ padding: 1rem; border-bottom: 1px solid var(--border); color: #4b5563; font-size: 0.95rem; }}
        tr:hover td {{ background: #f9fafb; }}
        .weekend td {{ background-color: var(--weekend-bg); color: var(--weekend-text); }}
        .summary-cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
        .card {{ background: #f8fafc; border: 1px solid #e2e8f0; padding: 1.5rem; border-radius: 8px; text-align: center; }}
        .card h3 {{ margin: 0 0 0.5rem 0; font-size: 0.875rem; color: #64748b; text-transform: uppercase; }}
        .card p {{ margin: 0; font-size: 1.75rem; font-weight: 700; color: #0f172a; }}
    </style>
</head>
<body>
    <h1>Dashboard Presenze Logistica</h1>
    <p class="subtitle">Dati aggiornati automaticamente dagli Excel</p>
    <div class="container">
        <div class="controls">
            <div class="btn-group">
                <button onclick="setFilterMode('day')" id="btn-day">Giorno</button>
                <button onclick="setFilterMode('week')" id="btn-week">Settimana</button>
                <button class="active" onclick="setFilterMode('month')" id="btn-month">Mese</button>
            </div>
            <div class="input-group" id="filter-container">
                <input type="month" id="dateFilter" onchange="renderData()">
            </div>
        </div>
        <div class="summary-cards">
            <div class="card"><h3>Totale Ore</h3><p id="sumHours">0</p></div>
            <div class="card"><h3>Totale Km Delta</h3><p id="sumKm">0</p></div>
            <div class="card"><h3>Autisti Attivi</h3><p id="sumDrivers">0</p></div>
        </div>
        <div style="overflow-x: auto;">
            <table>
                <thead>
                    <tr><th>Data</th><th>Giorno</th><th>Autista</th><th>Cliente</th><th>Ore</th><th>Delta Km</th><th>Inizio</th><th>Fine</th><th>Note</th></tr>
                </thead>
                <tbody id="tableBody"></tbody>
            </table>
        </div>
    </div>
    <script>
        const globalData = {dati_json_string};
        let currentMode = 'month';

        if (globalData.length > 0) {{
            const lastDate = new Date(globalData[globalData.length - 1].data);
            document.getElementById('dateFilter').value = lastDate.toISOString().substring(0, 7);
        }} else {{
            document.getElementById('dateFilter').value = new Date().toISOString().substring(0, 7);
        }}

        function setFilterMode(mode) {{
            currentMode = mode;
            document.querySelectorAll('.btn-group button').forEach(btn => btn.classList.remove('active'));
            document.getElementById(`btn-${{mode}}`).classList.add('active');

            const container = document.getElementById('filter-container');
            const currentDateVal = document.getElementById('dateFilter').value || (globalData.length > 0 ? globalData[globalData.length - 1].data.split('T')[0] : '');
            let dateObj = currentDateVal ? new Date(currentDateVal) : new Date();

            if (mode === 'day') {{
                container.innerHTML = '<input type="date" id="dateFilter" onchange="renderData()">';
                document.getElementById('dateFilter').value = dateObj.toISOString().split('T')[0];
            }} else if (mode === 'week') {{
                container.innerHTML = '<input type="week" id="dateFilter" onchange="renderData()">';
                document.getElementById('dateFilter').value = getWeek(dateObj);
            }} else if (mode === 'month') {{
                container.innerHTML = '<input type="month" id="dateFilter" onchange="renderData()">';
                document.getElementById('dateFilter').value = dateObj.toISOString().substring(0, 7);
            }}
            renderData();
        }}

        function getWeek(date) {{
            const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
            const dayNum = d.getUTCDay() || 7;
            d.setUTCDate(d.getUTCDate() + 4 - dayNum);
            const yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1));
            const weekNo = Math.ceil((((d - yearStart) / 86400000) + 1)/7);
            return `${{d.getUTCFullYear()}}-W${{weekNo.toString().padStart(2, '0')}}`;
        }}

        function renderData() {{
            const filterValue = document.getElementById('dateFilter').value;
            if (!filterValue) return;

            let filteredData = globalData.filter(item => {{
                const itemDate = new Date(item.data);
                if (currentMode === 'day') return item.data.startsWith(filterValue);
                if (currentMode === 'month') return item.data.startsWith(filterValue);
                if (currentMode === 'week') return getWeek(itemDate) === filterValue;
                return true;
            }});

            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';
            const giorniSettimana = ['Domenica', 'Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato'];
            let sumOre = 0, sumKm = 0, autistiSet = new Set();

            filteredData.forEach(item => {{
                const tr = document.createElement('tr');
                const dateObj = new Date(item.data);
                const dayName = giorniSettimana[dateObj.getDay()];
                if (dateObj.getDay() === 0 || dateObj.getDay() === 6) tr.classList.add('weekend');

                tr.innerHTML = `
                    <td>${{dateObj.toLocaleDateString('it-IT')}}</td>
                    <td><strong>${{dayName}}</strong></td>
                    <td>${{item.autista}}</td>
                    <td>${{item.cliente || '-'}}</td>
                    <td><strong>${{item.oreTotali || 0}}</strong></td>
                    <td>${{item.kmDelta || 0}}</td>
                    <td>${{item.oraInizioM || '-'}}</td>
                    <td>${{item.oraFineM || '-'}}</td>
                    <td title="${{item.note || ''}}">${{item.note || '-'}}</td>
                `;
                tbody.appendChild(tr);
                sumOre += parseFloat(item.oreTotali) || 0;
                sumKm += parseFloat(item.kmDelta) || 0;
                autistiSet.add(item.autista);
            }});

            if (filteredData.length === 0) {{
                tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 2rem; color: #9ca3af;">Nessun dato trovato per il periodo selezionato.</td></tr>';
            }}

            document.getElementById('sumHours').innerText = sumOre.toFixed(2);
            document.getElementById('sumKm').innerText = sumKm.toFixed(2);
            document.getElementById('sumDrivers').innerText = autistiSet.size;
        }}

        renderData();
    </script>
</body>
</html>
"""

html_path = os.path.join(cartella, "Dashboard_Presenze.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Dashboard generata con successo: {html_path}")
