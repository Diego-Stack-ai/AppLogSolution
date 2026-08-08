import time
import re
import io
from firebase_admin import storage
from infrastructure.firebase_setup import get_db
from core.utils import _safe_float
from firebase_functions import https_fn

AREA_RE_CLOUD = re.compile(r'(?:conto di|ordine e conto di)\s+[A-Z](\d{4,5})', re.I)
AREE_SPECIALI_FRUTTA = {"3198", "3199"}
AREE_SPECIALI_LATTE  = {"4199"}

def _estrai_area_da_storage(blob):
    """Apre un PDF DDT da Firebase Storage ed estrae il codice area numerico."""
    try:
        import pdfplumber
        pdf_bytes = blob.download_as_bytes()
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            text = pdf.pages[0].extract_text() or ""
            m = AREA_RE_CLOUD.search(text)
            if m:
                return m.group(1)
    except:
        pass
    return None

def handle_riepilogo_fatturazione(mese: str, anno: str, bucket_name: str, stats_callback=None, auth_context=None):
    """
    Scansiona tutti i DDT su Firebase Storage per il mese indicato.
    Restituisce i 4 contatori per la fatturazione:
      1. Frutta Standard   (tutti i DDT frutta tranne 3198/3199)
      2. Frutta Speciale   (DDT frutta con area 3198 o 3199)
      3. Latte Standard    (tutti i DDT latte tranne 4199)
      4. Latte Speciale    (DDT latte con area 4199)
    """
    if not auth_context:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.UNAUTHENTICATED,
            message="Non autorizzato."
        )

    start_time = time.time()

    if not mese or len(mese) != 2:
        return {"status": "errore", "message": "Mese non valido (usa MM, es: 04)", "errori": [], "data": {}}

    bucket = storage.bucket(name=bucket_name)
    prefix_base = "CONSEGNE/"

    # Cerca tutte le cartelle CONSEGNE del mese richiesto
    pattern_mese = f"-{mese}-{anno}"
    blobs_all = list(bucket.list_blobs(prefix=prefix_base))

    stats = {
        "FRUTTA": {"standard": 0, "speciali": 0, "dettaglio": {"3198": 0, "3199": 0}},
        "LATTE":  {"standard": 0, "speciali": 0, "dettaglio": {"4199": 0}}
    }
    cartelle_trovate = set()
    orfani = 0

    for blob in blobs_all:
        # Filtra solo i PDF dentro DDT-ORIGINALI-DIVISI del mese corretto
        path = blob.name
        if "DDT-ORIGINALI-DIVISI" not in path or not path.endswith(".pdf"):
            continue
        # Verifica che la cartella CONSEGNE_XX-MM-YYYY corrisponda al mese
        parts = path.split("/")
        if len(parts) < 2:
            continue
        cartella = parts[1]  # es. CONSEGNE_22-04-2026
        if pattern_mese not in cartella:
            continue

        cartelle_trovate.add(cartella)

        # Determina il tipo (FRUTTA o LATTE) dal percorso
        tipo = None
        if "/FRUTTA/" in path:
            tipo = "FRUTTA"
        elif "/LATTE/" in path:
            tipo = "LATTE"
        else:
            continue

        # Estrae il codice area dal PDF
        area = _estrai_area_da_storage(blob)

        if tipo == "FRUTTA":
            if area in AREE_SPECIALI_FRUTTA:
                stats["FRUTTA"]["speciali"] += 1
                if area in stats["FRUTTA"]["dettaglio"]:
                    stats["FRUTTA"]["dettaglio"][area] += 1
            else:
                stats["FRUTTA"]["standard"] += 1
                if not area:
                    orfani += 1
        else:  # LATTE
            if area in AREE_SPECIALI_LATTE:
                stats["LATTE"]["speciali"] += 1
                stats["LATTE"]["dettaglio"]["4199"] += 1
            else:
                stats["LATTE"]["standard"] += 1
                if not area:
                    orfani += 1

    tot_frutta  = stats["FRUTTA"]["standard"] + stats["FRUTTA"]["speciali"]
    tot_latte   = stats["LATTE"]["standard"]  + stats["LATTE"]["speciali"]
    tot_generale = tot_frutta + tot_latte

    db = get_db()
    VALORE_DDT_STANDARD = 16.50
    VALORE_DDT_SPECIALE = 16.50
    # Fetch listino from Firestore
    try:
        dnr_doc = db.collection("clienti").document("DNR").collection("impostazioni").document("listino").get()
        if dnr_doc.exists:
            listino_dnr = dnr_doc.to_dict()
            VALORE_DDT_STANDARD = _safe_float(listino_dnr.get("tariffa_ddt", 16.50)) or 16.50
            VALORE_DDT_SPECIALE = VALORE_DDT_STANDARD
    except Exception as e:
        print(f"Errore lettura listino DNR: {e}")

    fatturato_frutta_std  = round(stats["FRUTTA"]["standard"] * VALORE_DDT_STANDARD, 2)
    fatturato_frutta_spec = round(stats["FRUTTA"]["speciali"] * VALORE_DDT_SPECIALE, 2)
    fatturato_latte_std   = round(stats["LATTE"]["standard"]  * VALORE_DDT_STANDARD, 2)
    fatturato_latte_spec  = round(stats["LATTE"]["speciali"]  * VALORE_DDT_SPECIALE, 2)
    fatturato_totale      = round(fatturato_frutta_std + fatturato_frutta_spec +
                                   fatturato_latte_std  + fatturato_latte_spec, 2)

    elapsed = time.time() - start_time
    if stats_callback:
        stats_callback("riepilogo_fatturazione", elapsed)

    return {
        "status": "ok",
        "message": f"Riepilogo {mese}/{anno}: {tot_generale} DDT in {elapsed:.1f}s",
        "errori": [f"{orfani} DDT senza codice area (conteggiati come Standard)"] if orfani else [],
        "data": {
            "mese": mese, "anno": anno,
            "cartelle_elaborate": len(cartelle_trovate),
            "frutta": {
                "standard":   stats["FRUTTA"]["standard"],
                "speciali":   stats["FRUTTA"]["speciali"],
                "dettaglio":  stats["FRUTTA"]["dettaglio"],
                "fatturato_standard":  fatturato_frutta_std,
                "fatturato_speciali":  fatturato_frutta_spec,
                "totale":     tot_frutta
            },
            "latte": {
                "standard":   stats["LATTE"]["standard"],
                "speciali":   stats["LATTE"]["speciali"],
                "dettaglio":  stats["LATTE"]["dettaglio"],
                "fatturato_standard":  fatturato_latte_std,
                "fatturato_speciali":  fatturato_latte_spec,
                "totale":     tot_latte
            },
            "totale_generale":    tot_generale,
            "fatturato_totale":   fatturato_totale,
            "valore_ddt_euro":    VALORE_DDT_STANDARD,
            "tempo_sec":          elapsed
        }
    }
