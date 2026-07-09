import sys

filepath = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend\firebase-auth-sync.js"

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(filepath, 'r', encoding='latin-1') as f:
        content = f.read()

# Replace line 2
old_import = 'import { getFirestore, collection, doc, getDoc, updateDoc, setDoc, deleteDoc, onSnapshot, addDoc } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";'
new_import = 'import { getFirestore, collection, doc, getDoc, updateDoc, setDoc, deleteDoc, onSnapshot, addDoc, query, where } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";'
content = content.replace(old_import, new_import)

# Inject Toast logic at the end of startRealtimeSync
target_str = """      const unsubGiustificativi = onSnapshot(collection(db, "giustificativi"), (snapshot) => {
          const giustificativi = [];
          snapshot.forEach((d) => {
              giustificativi.push({ id: d.id, ...d.data() });
          });
          window.appData.lista_giustificativi = giustificativi;
          if (typeof window.renderGiustificativi === 'function') window.renderGiustificativi();
      });
      activeListeners.push(unsubGiustificativi);
  }
  
  // 🛒 CRUD PROGETTI 🛒"""

new_str = """      const unsubGiustificativi = onSnapshot(collection(db, "giustificativi"), (snapshot) => {
          const giustificativi = [];
          snapshot.forEach((d) => {
              giustificativi.push({ id: d.id, ...d.data() });
          });
          window.appData.lista_giustificativi = giustificativi;
          if (typeof window.renderGiustificativi === 'function') window.renderGiustificativi();
      });
      activeListeners.push(unsubGiustificativi);
      
      // NOTIFICHE RESI/RITIRI IN TEMPO REALE (Solo per Admin)
      if (isAdmin) {
          const todayStr = new Date().toISOString().split("T")[0]; // YYYY-MM-DD
          const qResi = query(
              collection(db, "clienti", "DNR", "resi_e_ritiri"),
              where("data_evento", "==", todayStr),
              where("letto_da_ufficio", "==", false)
          );
          const unsubResi = onSnapshot(qResi, (snapshot) => {
              snapshot.docChanges().forEach((change) => {
                  if (change.type === "added") {
                      showResoToast(change.doc.id, change.doc.data(), db);
                  }
                  if (change.type === "removed" || change.type === "modified") {
                      const data = change.doc.data();
                      if(data.letto_da_ufficio || change.type === "removed") {
                          const toast = document.getElementById(`toast-${change.doc.id}`);
                          if(toast) toast.remove();
                      }
                  }
              });
          });
          activeListeners.push(unsubResi);
      }
  }

function showResoToast(docId, data, db) {
    if(document.getElementById(`toast-${docId}`)) return;
    
    const container = document.getElementById("toast-container") || createToastContainer();
    
    const t = document.createElement("div");
    t.id = `toast-${docId}`;
    t.style.cssText = "background:white; border-left:5px solid #ef4444; border-radius:8px; box-shadow:0 4px 15px rgba(0,0,0,0.15); padding:15px; margin-bottom:15px; width:300px; font-family:'Outfit',sans-serif; animation: slideIn 0.3s ease-out; position:relative;";
    
    const iconStr = data.tipo_segnalazione === "merce_rotta" ? "🔴 Rifiuto/Rotta" : "🔵 Reso/Ritiro";
    
    t.innerHTML = `
        <h4 style="margin:0 0 5px 0; font-size:14px;">${iconStr}</h4>
        <p style="margin:0 0 5px 0; font-size:13px; color:#475569;">Cliente: <b>${data.nome_cliente || data.codice_cliente}</b></p>
        <p style="margin:0 0 10px 0; font-size:12px; color:#94a3b8;">Giro: ${data.id_viaggio}</p>
        <div style="display:flex; gap:10px;">
            <a href="${data.url_foto}" target="_blank" style="flex:1; background:#f1f5f9; color:#475569; padding:8px; text-align:center; text-decoration:none; border-radius:6px; font-size:12px; font-weight:bold;">Vedi Foto</a>
            <button id="btn-letto-${docId}" style="flex:1; background:#10b981; color:white; border:none; padding:8px; border-radius:6px; cursor:pointer; font-size:12px; font-weight:bold;">Letto</button>
        </div>
    `;
    
    container.appendChild(t);
    
    document.getElementById(`btn-letto-${docId}`).addEventListener('click', async () => {
        try {
            document.getElementById(`btn-letto-${docId}`).innerText = "...";
            await updateDoc(doc(db, "clienti", "DNR", "resi_e_ritiri", docId), { letto_da_ufficio: true });
            t.remove();
        } catch(e) {
            console.error("Errore segna come letto", e);
            document.getElementById(`btn-letto-${docId}`).innerText = "Letto";
        }
    });
}

function createToastContainer() {
    const c = document.createElement("div");
    c.id = "toast-container";
    c.style.cssText = "position:fixed; top:70px; right:20px; z-index:99999;";
    
    const style = document.createElement("style");
    style.innerHTML = "@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }";
    document.head.appendChild(style);
    
    document.body.appendChild(c);
    return c;
}
  
  // 🛒 CRUD PROGETTI 🛒"""

# The target_str contains emojis that might fail to match if encoded differently.
# So let's replace the block programmatically by finding the end of startRealtimeSync instead of matching emojis.

# Let's find "activeListeners.push(unsubGiustificativi);"
if "activeListeners.push(unsubGiustificativi);" in content:
    idx = content.find("activeListeners.push(unsubGiustificativi);")
    idx = content.find("}", idx)
    if idx != -1:
        # replace the } with our new logic
        first_part = content[:idx]
        second_part = content[idx+1:]
        
        injection = """
      // NOTIFICHE RESI/RITIRI IN TEMPO REALE (Solo per Admin)
      if (isAdmin) {
          const todayStr = new Date().toISOString().split("T")[0]; // YYYY-MM-DD
          const qResi = query(
              collection(db, "clienti", "DNR", "resi_e_ritiri"),
              where("data_evento", "==", todayStr),
              where("letto_da_ufficio", "==", false)
          );
          const unsubResi = onSnapshot(qResi, (snapshot) => {
              snapshot.docChanges().forEach((change) => {
                  if (change.type === "added") {
                      showResoToast(change.doc.id, change.doc.data(), db);
                  }
                  if (change.type === "removed" || change.type === "modified") {
                      const data = change.doc.data();
                      if(data.letto_da_ufficio || change.type === "removed") {
                          const toast = document.getElementById(`toast-${change.doc.id}`);
                          if(toast) toast.remove();
                      }
                  }
              });
          });
          activeListeners.push(unsubResi);
      }
  }

function showResoToast(docId, data, db) {
    if(document.getElementById(`toast-${docId}`)) return;
    
    const container = document.getElementById("toast-container") || createToastContainer();
    
    const t = document.createElement("div");
    t.id = `toast-${docId}`;
    t.style.cssText = "background:white; border-left:5px solid #ef4444; border-radius:8px; box-shadow:0 4px 15px rgba(0,0,0,0.15); padding:15px; margin-bottom:15px; width:300px; font-family:'Outfit',sans-serif; animation: slideIn 0.3s ease-out; position:relative;";
    
    const iconStr = data.tipo_segnalazione === "merce_rotta" ? "🔴 Rifiuto/Rotta" : "🔵 Reso/Ritiro";
    
    t.innerHTML = `
        <h4 style="margin:0 0 5px 0; font-size:14px;">${iconStr}</h4>
        <p style="margin:0 0 5px 0; font-size:13px; color:#475569;">Cliente: <b>${data.nome_cliente || data.codice_cliente}</b></p>
        <p style="margin:0 0 10px 0; font-size:12px; color:#94a3b8;">Giro: ${data.id_viaggio}</p>
        <div style="display:flex; gap:10px;">
            <a href="${data.url_foto}" target="_blank" style="flex:1; background:#f1f5f9; color:#475569; padding:8px; text-align:center; text-decoration:none; border-radius:6px; font-size:12px; font-weight:bold;">Vedi Foto</a>
            <button id="btn-letto-${docId}" style="flex:1; background:#10b981; color:white; border:none; padding:8px; border-radius:6px; cursor:pointer; font-size:12px; font-weight:bold;">Letto</button>
        </div>
    `;
    
    container.appendChild(t);
    
    document.getElementById(`btn-letto-${docId}`).addEventListener('click', async () => {
        try {
            document.getElementById(`btn-letto-${docId}`).innerText = "...";
            await updateDoc(doc(db, "clienti", "DNR", "resi_e_ritiri", docId), { letto_da_ufficio: true });
            t.remove();
        } catch(e) {
            console.error("Errore segna come letto", e);
            document.getElementById(`btn-letto-${docId}`).innerText = "Letto";
        }
    });
}

function createToastContainer() {
    const c = document.createElement("div");
    c.id = "toast-container";
    c.style.cssText = "position:fixed; top:70px; right:20px; z-index:99999;";
    
    const style = document.createElement("style");
    style.innerHTML = "@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }";
    document.head.appendChild(style);
    
    document.body.appendChild(c);
    return c;
}
"""
        content = first_part + injection + second_part

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
