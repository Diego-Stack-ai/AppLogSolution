import os
import subprocess
import sys
import shutil
import hashlib
import json
from datetime import datetime

STATE_FILE = os.path.join('e2e-tests', '.qa-state.json')
BASELINE_BACKUP = 'sw.js.qa-baseline.backup'

def get_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def check_environment():
    try:
        branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
        if branch != 'sviluppo':
            print("ERRORE: Branch attuale non è 'sviluppo'.")
            sys.exit(1)
        with open('.firebaserc', 'r') as f:
            if 'log-solutions-sviluppo' not in f.read():
                print("ERRORE: log-solutions-sviluppo non in .firebaserc.")
                sys.exit(1)
    except Exception as e:
        sys.exit(1)

def main():
    print("=== PREPARAZIONE TEST 8 (Baseline e Update) ===")
    check_environment()
    
    sw_path = os.path.join('frontend', 'sw.js')
    
    # Crea backup immutabile solo se non esiste
    if not os.path.exists(BASELINE_BACKUP):
        print("Creazione backup baseline immutabile...")
        shutil.copy2(sw_path, BASELINE_BACKUP)
        
    baseline_hash = get_sha256(BASELINE_BACKUP)
    
    # Estrazione versione baseline (semplificata per demo)
    baseline_version = "6.254"
    
    # Crea o aggiorna lo stato
    state = {
        "baseline_version": baseline_version,
        "test8_version": None,
        "test9_version": None,
        "backup_path": BASELINE_BACKUP,
        "baseline_hash": baseline_hash,
        "firebase_project": "log-solutions-sviluppo",
        "phase": "PREPARE_TEST_8_DONE"
    }
    
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)
        
    print(f"Stato QA salvato. Hash baseline: {baseline_hash}")
    
    # TODO: Logica bump_version.py e Deploy Hosting se autorizzati.
    print("Pronto per il Test 8. (Bump e Deploy OFF)")

if __name__ == "__main__":
    main()
