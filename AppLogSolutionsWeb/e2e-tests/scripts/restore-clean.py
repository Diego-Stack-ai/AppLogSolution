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
    print("=== RIPRISTINO PULITO ===")
    
    if not os.path.exists(STATE_FILE):
        print("ERRORE: Stato QA mancante.")
        sys.exit(1)
        
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)
        
    if not os.path.exists(BASELINE_BACKUP) or get_sha256(BASELINE_BACKUP) != state["baseline_hash"]:
        print("ERRORE CRITICO: Backup baseline corrotto o inesistente. Impossibile ripristinare con sicurezza.")
        sys.exit(1)
        
    sw_path = os.path.join('frontend', 'sw.js')
    
    # 1. Ripristino esclusivo dal backup immutabile
    shutil.copy2(BASELINE_BACKUP, sw_path)
    print("sw.js ripristinato dal backup immutabile.")
    
    # 2. Controllo coerenza hash dopo ripristino
    if get_sha256(sw_path) != state["baseline_hash"]:
        print("ERRORE: l'hash del file ripristinato non coincide.")
        sys.exit(1)
        
    # TODO: Logica bump finale pulito ed eventuale deploy
    
    print("Pronto per chiusura QA (Deploy OFF)")
    # Pulizia post-deploy se richiesto.

if __name__ == "__main__":
    main()
