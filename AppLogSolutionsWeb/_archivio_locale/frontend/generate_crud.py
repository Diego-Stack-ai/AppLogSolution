import os
import re

template_html = '''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TITLE} - Log Solution</title>
    <link rel="stylesheet" href="styles.css?v=1.36">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
    <link rel="manifest" href="manifest.json">
    <style>
        .list-container { display: grid; gap: 16px; margin-top:20px; }
        .data-card { background: var(--surface); border: 1px solid var(--border); border-radius: 20px; padding: 20px; }
        .data-card { border-left: 5px solid {BORDERColor}; }
    </style>
</head>
<body>
    <nav class="glass-nav">
        <div class="nav-content">
            <button onclick="window.history.back()" class="logout-btn" style="border:none; background:none; cursor:pointer; margin-right:8px; display:flex;">
                <span class="material-icons-round">arrow_back</span>
            </button>
            <div class="nav-title" style="flex: 1;">{TITLE}</div>
            <a href="login.html" class="logout-btn" title="Esci"><span class="material-icons-round">logout</span></a>
        </div>
    </nav>

    <main class="main-container">
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <input type="text" id="searchInput" placeholder="Cerca..." style="flex:1; padding: 12px; border-radius: 12px; border: 1px solid #e2e8f0;">
            <button class="btn-primary" onclick="openModal()" style="border-radius: 12px; padding: 0 20px;">+ Nuovo</button>
        </div>
        <div id="loadingIndicator">Caricamento in corso...</div>
        <div id="dataContainer" class="list-container"></div>
    </main>

    <!-- Modal Form -->
    <div id="dataModal" class="modal-overlay">
        <div class="modal-content">
            <h3 style="margin-bottom: 20px;">Gestione {TITLE}</h3>
            <form id="dataForm" class="modal-body" style="display: grid; gap: 15px;">
                <input type="hidden" id="editId">
                <div id="dynamicFields" style="display: grid; gap: 15px;"></div>
                <div style="display: flex; gap: 10px; margin-top: 20px;">
                    <button type="submit" class="btn-primary" style="flex: 2;">Salva</button>
                    <button type="button" onclick="closeModal()" class="btn-primary" style="flex: 1; background: #f1f5f9; color: #64748b; box-shadow: none;">Annulla</button>
                </div>
            </form>
        </div>
    </div>

    <script type="module">
        import { getFirestore, collection, doc, addDoc, setDoc, deleteDoc, onSnapshot } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
        import { getApps, initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
        import { firebaseConfig } from "./firebase-config.js";
        const app = getApps().length ? getApps()[0] : initializeApp(firebaseConfig);
        const db = getFirestore(app);

        const COLL_PATH = {COLL_PATH};
        const FIELDS = {FIELDS};
        let items = [];

        onSnapshot(collection(db, ...COLL_PATH), (snapshot) => {
            items = [];
            snapshot.forEach(d => items.push({ id: d.id, ...d.data() }));
            document.getElementById('loadingIndicator').style.display = 'none';
            renderTable();
        });

        document.getElementById('searchInput').addEventListener('input', renderTable);

        window.renderTable = function() {
            const q = document.getElementById('searchInput').value.toLowerCase();
            const filtered = items.filter(i => JSON.stringify(i).toLowerCase().includes(q));
            
            const html = filtered.map(item => {
                let details = '';
                Object.keys(item).forEach(k => {
                    if(k!=='id') details += <div style="font-size:13px; color:#475569;"><b>\:</b> \</div>;
                });
                return 
                <div class="data-card">
                    <div style="display: flex; justify-content: space-between;">
                        <div>\</div>
                        <div style="display:flex; gap:10px; flex-direction:column;">
                            <button onclick="editItem('\')" style="background:#4f46e5; color:white; border:none; padding:8px; border-radius:8px; cursor:pointer;"><span class="material-icons-round" style="font-size: 16px;">edit</span></button>
                            <button onclick="deleteItem('\')" style="background:#ef4444; color:white; border:none; padding:8px; border-radius:8px; cursor:pointer;"><span class="material-icons-round" style="font-size: 16px;">delete</span></button>
                        </div>
                    </div>
                </div>;
            }).join('');
            document.getElementById('dataContainer').innerHTML = html || '<div style="padding: 20px; color: #64748b;">Nessun dato.</div>';
        }

        window.openModal = function() {
            document.getElementById('editId').value = '';
            document.getElementById('dataForm').reset();
            buildFields({});
            document.getElementById('dataModal').classList.add('active');
        }

        window.closeModal = function() {
            document.getElementById('dataModal').classList.remove('active');
        }

        window.editItem = function(id) {
            const item = items.find(i => i.id === id);
            document.getElementById('editId').value = id;
            buildFields(item);
            document.getElementById('dataModal').classList.add('active');
        }

        window.deleteItem = async function(id) {
            if(confirm('Eliminare questo elemento?')) {
                await deleteDoc(doc(db, ...COLL_PATH, id));
            }
        }

        function buildFields(item) {
            const container = document.getElementById('dynamicFields');
            let html = '';
            FIELDS.forEach(f => {
                const val = item[f] || '';
                html += 
                <div style="display:flex; flex-direction:column; gap:5px;">
                    <label style="font-size:12px; font-weight:bold; color:var(--primary); text-transform:uppercase;">\</label>
                    <input type="text" id="f_\" value="\" style="padding:10px; border-radius:8px; border:1px solid #cbd5e1; font-size:14px;">
                </div>;
            });
            container.innerHTML = html;
        }

        document.getElementById('dataForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const id = document.getElementById('editId').value;
            const data = {};
            FIELDS.forEach(f => { data[f] = document.getElementById('f_'+f).value; });

            if(id) {
                await setDoc(doc(db, ...COLL_PATH, id), data, { merge: true });
            } else {
                await addDoc(collection(db, ...COLL_PATH), data);
            }
            closeModal();
        });
    </script>
</body>
</html>'''

pages = [
    {
        "file": "gestione_articoli.html",
        "title": "Gestione Articoli (Anagrafica)",
        "color": "#f59e0b",
        "path": "['customers', 'DNR', 'anagrafica_articoli']",
        "fields": "['codice', 'descrizione', 'confezionamento', 'unita_principale', 'unita_secondaria', 'ratio', 'porzioni_unita']"
    },
    {
        "file": "gestione_nuovi_clienti.html",
        "title": "Gestione Nuovi Clienti (Anomalie)",
        "color": "#3b82f6",
        "path": "['customers', 'DNR', 'gestione_nuovi_clienti']",
        "fields": "['Codice Frutta', 'Codice Latte', 'A chi va consegnato', 'Indirizzo', 'CAP', 'Città', 'Provincia', 'Orario min', 'Orario max', 'Tipologia consegna']"
    },
    {
        "file": "gestione_orari.html",
        "title": "Gestione Orari Mancanti",
        "color": "#ef4444",
        "path": "['customers', 'DNR', 'gestione_orari_mancanti']",
        "fields": "['Codice Cliente', 'Nome', 'Indirizzo', 'Orario Mancante', 'Note']"
    },
    {
        "file": "gestione_rientri.html",
        "title": "Gestione Rientri",
        "color": "#d946ef",
        "path": "['customers', 'DNR', 'gestione_rientri']",
        "fields": "['Data DDT', 'Codice consegna', 'Stato', 'Note']"
    }
]

import os
for p in pages:
    html = template_html.replace('{TITLE}', p['title'])
    html = html.replace('{BORDERColor}', p['color'])
    html = html.replace('{COLL_PATH}', p['path'])
    html = html.replace('{FIELDS}', p['fields'])
    with open('G:/Il mio Drive/App/AppLogSolutions/frontend/' + p['file'], 'w', encoding='utf-8') as f:
        f.write(html)
        print("Scritto:", p['file'])

