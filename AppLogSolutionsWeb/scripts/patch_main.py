import re
import codecs
import json

with codecs.open('functions/main.py', 'r', 'utf-8') as f:
    content = f.read()

cache_manager = """
def get_db():
    return firestore.client()

# --- STORAGE CACHES ---
_LOCAL_STORAGE_CACHES = {
    "distanze_reali_cache.json": None,
    "directions_cache.json": None,
    "distanze_traffico_cache.json": None
}

def _load_storage_cache(filename):
    global _LOCAL_STORAGE_CACHES
    if _LOCAL_STORAGE_CACHES[filename] is not None:
        return _LOCAL_STORAGE_CACHES[filename]
        
    try:
        bucket = storage.bucket()
        blob = bucket.blob(f"caches/{filename}")
        if blob.exists():
            data_str = blob.download_as_string().decode("utf-8")
            _LOCAL_STORAGE_CACHES[filename] = json.loads(data_str)
        else:
            import os
            local_path = os.path.join(os.path.dirname(__file__), "caches", filename)
            if os.path.exists(local_path):
                with open(local_path, "r", encoding="utf-8") as f:
                    _LOCAL_STORAGE_CACHES[filename] = json.load(f)
                blob.upload_from_filename(local_path, content_type="application/json")
            else:
                _LOCAL_STORAGE_CACHES[filename] = {}
    except Exception as e:
        print(f"[CACHE] Errore load {filename}: {e}")
        _LOCAL_STORAGE_CACHES[filename] = {}
        
    return _LOCAL_STORAGE_CACHES[filename]

def _save_storage_cache(filename):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(f"caches/{filename}")
        blob.upload_from_string(json.dumps(_LOCAL_STORAGE_CACHES[filename], ensure_ascii=False), content_type="application/json")
    except Exception as e:
        print(f"[CACHE] Errore save {filename}: {e}")
"""
content = content.replace("def get_db():\n    return firestore.client()", cache_manager)

re_leggi_cache = r"def _leggi_cache_firestore\(p1, p2\):[\s\S]*?return None"
new_leggi_cache = """def _leggi_cache_firestore(p1, p2):
    cache = _load_storage_cache("distanze_reali_cache.json")
    key = _cache_key(p1, p2)
    val = cache.get(key)
    if val: return val.get('dist')
    rev_key = _cache_key(p2, p1)
    val_rev = cache.get(rev_key)
    if val_rev: return val_rev.get('dist')
    return None"""
content = re.sub(re_leggi_cache, new_leggi_cache, content)

re_scrivi_cache = r"def _scrivi_cache_firestore\(coppie\):[\s\S]*?print\(f\"\[CACHE\] Errore scrittura Firestore: \{e\}\"\)"
new_scrivi_cache = """def _scrivi_cache_firestore(coppie):
    if not coppie: return
    cache = _load_storage_cache("distanze_reali_cache.json")
    for key, dist, dur in coppie:
        cache[key] = {'dist': dist, 'dur': dur}
    _save_storage_cache("distanze_reali_cache.json")
    print(f"[CACHE] Scritte {len(coppie)} nuove distanze su Storage.")"""
content = re.sub(re_scrivi_cache, new_scrivi_cache, content)

re_leggi_percorsi = r"def _leggi_percorsi_cache\(key\):[\s\S]*?return None"
new_leggi_percorsi = """def _leggi_percorsi_cache(key):
    cache = _load_storage_cache("directions_cache.json")
    return cache.get(key)"""
content = re.sub(re_leggi_percorsi, new_leggi_percorsi, content)

re_scrivi_percorsi = r"def _scrivi_percorsi_cache\(key, data\):[\s\S]*?print\(f\"\[CACHE\] Errore scrittura percorsi_stradali_cache: \{e\}\"\)"
new_scrivi_percorsi = """def _scrivi_percorsi_cache(key, data):
    cache = _load_storage_cache("directions_cache.json")
    cache[key] = data
    _save_storage_cache("directions_cache.json")"""
content = re.sub(re_scrivi_percorsi, new_scrivi_percorsi, content)

re_leggi_completa = r"def _leggi_cache_completa_firestore\(p1, p2\):[\s\S]*?return None"
new_leggi_completa = """def _leggi_cache_completa_firestore(p1, p2):
    cache = _load_storage_cache("distanze_reali_cache.json")
    key = _cache_key(p1, p2)
    val = cache.get(key)
    if val: return val
    rev_key = _cache_key(p2, p1)
    val_rev = cache.get(rev_key)
    if val_rev: return val_rev
    return None"""
content = re.sub(re_leggi_completa, new_leggi_completa, content)

re_leggi_traffic = r"def _leggi_traffic_cache\(p1, p2, slot_str\):[\s\S]*?return None"
new_leggi_traffic = """def _leggi_traffic_cache(p1, p2, slot_str):
    cache = _load_storage_cache("distanze_traffico_cache.json")
    key = _cache_key(p1, p2)
    val = cache.get(key)
    if val: return val.get(slot_str)
    rev_key = _cache_key(p2, p1)
    val_rev = cache.get(rev_key)
    if val_rev: return val_rev.get(slot_str)
    return None"""
content = re.sub(re_leggi_traffic, new_leggi_traffic, content)

re_scrivi_traffic = r"def _scrivi_traffic_cache\(p1, p2, slot_str, dur_sec\):[\s\S]*?pass"
new_scrivi_traffic = """def _scrivi_traffic_cache(p1, p2, slot_str, dur_sec):
    try:
        cache = _load_storage_cache("distanze_traffico_cache.json")
        key = _cache_key(p1, p2)
        if key not in cache: cache[key] = {}
        cache[key][slot_str] = int(dur_sec)
        _save_storage_cache("distanze_traffico_cache.json")
    except:
        pass"""
content = re.sub(re_scrivi_traffic, new_scrivi_traffic, content)

content = content.replace("search_parameters.time_limit.seconds = 4", "search_parameters.time_limit.seconds = 10")
content = content.replace("params.time_limit.seconds = 8", "params.time_limit.seconds = 10")

with codecs.open('functions/main.py', 'w', 'utf-8') as f:
    f.write(content)

print("Patch applied.")
