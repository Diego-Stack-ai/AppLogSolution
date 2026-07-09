import re

filepath = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend\mappa_zone.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports
old_import = 'import { getFirestore, collection, doc, getDocs, setDoc, onSnapshot, updateDoc, arrayUnion } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";'
new_import = 'import { getFirestore, collection, doc, getDocs, setDoc, onSnapshot, updateDoc, arrayUnion, query, where } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";'
content = content.replace(old_import, new_import)

# 2. Add global variable viaggiTimestamps
if "let viaggiTimestamps = {};" not in content:
    content = content.replace("let DATA_ZONE = [];", "let DATA_ZONE = [];\n          let viaggiTimestamps = {}; // { id_zona: timestamp }")

# 3. Load timestamps after loading JSON
load_json_target = "updateTotals();"
load_json_injection = """              // --- CARICAMENTO TIMESTAMP VIAGGI ---
              try {
                  const q = query(collection(db, 'clienti/DNR/viaggi ddt'), where('data_lavoro', '==', targetFileDate));
                  const snap = await getDocs(q);
                  snap.forEach(doc => {
                      const id_zona = doc.id.split('_')[1];
                      const data = doc.data();
                      if(data.ultimo_aggiornamento) {
                          viaggiTimestamps[id_zona] = data.ultimo_aggiornamento.toMillis ? data.ultimo_aggiornamento.toMillis() : new Date(data.ultimo_aggiornamento).getTime();
                      }
                  });
              } catch(e) {
                  console.warn("Impossibile caricare timestamps:", e);
              }

              updateTotals();"""
content = content.replace(load_json_target, load_json_injection, 1)

# 4. Check timestamps before saving in saveDataGlobale
save_target = """window.saveDataGlobale = async function(isBackground = false) {"""
save_injection = """window.saveDataGlobale = async function(isBackground = false) {
              // --- CONTROLLO CONFLITTI (LOCK TIMESTAMP) ---
              if (!isBackground) {
                  try {
                      const q = query(collection(db, 'clienti/DNR/viaggi ddt'), where('data_lavoro', '==', targetFileDate));
                      const snap = await getDocs(q);
                      let conflitto = false;
                      let nomeConflitto = "";
                      snap.forEach(doc => {
                          const id_zona = doc.id.split('_')[1];
                          const data = doc.data();
                          if(data.ultimo_aggiornamento) {
                              const currentTs = data.ultimo_aggiornamento.toMillis ? data.ultimo_aggiornamento.toMillis() : new Date(data.ultimo_aggiornamento).getTime();
                              if (viaggiTimestamps[id_zona] && currentTs > viaggiTimestamps[id_zona]) {
                                  conflitto = true;
                                  nomeConflitto = data.nome_giro || id_zona;
                              }
                          }
                      });
                      if (conflitto) {
                          Swal.fire('Conflitto Rilevato', `Il giro ${nomeConflitto} è stato modificato dall'autista mentre avevi questa pagina aperta. Ricarica la pagina per vedere le sue modifiche ed evitare di sovrascriverle.`, 'error');
                          return; // Blocca il salvataggio
                      }
                  } catch(e) {
                      console.warn("Errore controllo conflitti:", e);
                  }
              }"""
content = content.replace(save_target, save_injection)

# 5. Check timestamps in aggiornaModificati
aggiorna_target = """        window.aggiornaModificati = async () => {
            const modificati = DATA_ZONE.filter(z => z._stato === 'modificato').map(z => z.id_zona);"""
aggiorna_injection = """        window.aggiornaModificati = async () => {
            const modificati = DATA_ZONE.filter(z => z._stato === 'modificato').map(z => z.id_zona);
            // --- CONTROLLO CONFLITTI (LOCK TIMESTAMP) ---
            try {
                const q = query(collection(db, 'clienti/DNR/viaggi ddt'), where('data_lavoro', '==', targetFileDate));
                const snap = await getDocs(q);
                let conflitto = false;
                let nomeConflitto = "";
                snap.forEach(doc => {
                    const id_zona = doc.id.split('_')[1];
                    const data = doc.data();
                    if(data.ultimo_aggiornamento) {
                        const currentTs = data.ultimo_aggiornamento.toMillis ? data.ultimo_aggiornamento.toMillis() : new Date(data.ultimo_aggiornamento).getTime();
                        if (viaggiTimestamps[id_zona] && currentTs > viaggiTimestamps[id_zona]) {
                            conflitto = true;
                            nomeConflitto = data.nome_giro || id_zona;
                        }
                    }
                });
                if (conflitto) {
                    Swal.fire('Conflitto Rilevato', `Il giro ${nomeConflitto} è stato modificato dall'autista mentre avevi questa pagina aperta. Ricarica la pagina per evitare di sovrascrivere.`, 'error');
                    return; // Blocca il salvataggio
                }
            } catch(e) {
                console.warn("Errore controllo conflitti:", e);
            }"""
content = content.replace(aggiorna_target, aggiorna_injection)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
