import os
import subprocess
import sys
import shutil
import hashlib
import json

STATE_FILE = os.path.join('e2e-tests', '.qa-state.json')
BASELINE_BACKUP = 'sw.js.qa-baseline.backup'

def get_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def main():
    print("=== PREPARAZIONE TEST 9 (Critico Locale) ===")
    
    # 1. Verifiche di sicurezza
    branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
    if branch != 'sviluppo':
        print("ERRORE: Non su ramo sviluppo.")
        sys.exit(1)
        
    if not os.path.exists(STATE_FILE):
        print("ERRORE: Stato QA mancante. Eseguire Test 8 prima.")
        sys.exit(1)
        
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)
        
    if state.get("phase") not in ["TEST_8_COMPLETED", "BASELINE_BACKUP_CREATED"]:
        print("ERRORE: Test 8 / Baseline non concluso nel qa-state.")
        sys.exit(1)
        
    BASELINE_BACKUP_PATH = os.path.join('e2e-tests', '.qa-backups', BASELINE_BACKUP)
    if not os.path.exists(BASELINE_BACKUP_PATH) or get_sha256(BASELINE_BACKUP_PATH).lower() != state.get("sw_js_hash", state.get("baseline_hash", "")).lower():
        print(f"ERRORE: Backup baseline corrotto o inesistente. ({BASELINE_BACKUP_PATH})")
        sys.exit(1)
        
    sw_path = os.path.join('frontend', 'sw.js')
    
    # Inserimento asset fasullo
    with open(sw_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'CRITICAL_ASSETS = [' in content:
        content = content.replace('CRITICAL_ASSETS = [', 'CRITICAL_ASSETS = [\n    "./script-INVENTATO.js",')
        with open(sw_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Asset critico fasullo inserito.")
    
    # Aggiorna stato
    state["phase"] = "PREPARE_TEST_9_DONE"
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)
        
    print("Pronto per il Test 9. (Bump e Deploy OFF)")

if __name__ == "__main__":
    main()
