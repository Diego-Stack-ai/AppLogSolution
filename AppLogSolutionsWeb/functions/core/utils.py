import re

_PHONE_RE = re.compile(r'(?:\+39)?[\s\-]?(?:0\d{1,4}[\s\-]?\d{4,8}|3\d{2}[\s\-]?\d{6,7})')

def _safe_float(val):
    try:
        if val is None:
            return None
        s = str(val).strip().replace(",", ".")
        if not s:
            return None
        return float(s)
    except (ValueError, TypeError):
        return None

def clean_client_code(code_val):
    if code_val is None or (hasattr(code_val, "isna") and code_val.isna()):
        return ""
    code_str = str(code_val).strip()
    if code_str.endswith(".0"):
        code_str = code_str[:-2]
    return code_str

def _extract_phone(p):
    """Estrae e normalizza un numero di telefono dal punto di consegna."""
    tel = str(p.get('telefono', p.get('tel', p.get('phone', ''))) or '').strip()
    if not tel:
        note_text = str(p.get('note', p.get('nota_integrativa', p.get('Note', ''))) or '')
        m = _PHONE_RE.search(note_text)
        if m:
            tel = m.group(0).strip()
    return re.sub(r'[\s\-]', '', tel) if tel else ''

def _build_tripla_chiave(cod_f: str, cod_l: str, nome: str) -> str:
    """
    Costruisce la chiave univoca: COD_F|COD_L|NOME (normalizzati lowercase).
    Questa chiave identifica univocamente il cliente anche se ha p00000 come codice.
    """
    cf = str(cod_f).strip().lower()
    cl = str(cod_l).strip().lower()
    n  = str(nome).strip().lower()
    return f"{cf}|{cl}|{n}"

def normalize_code(raw, articoli_noti):
    righe = [l.strip() for l in str(raw).split('\n') if l.strip() and not l.strip().startswith("Codice:")]
    if not righe: return "", ""
    code_base, idx_base = "", -1
    for i, r in enumerate(righe):
        if r.upper() in articoli_noti:
            code_base, idx_base = r, i
            break
        for prefix in articoli_noti:
            if prefix.endswith('-') and r.upper().startswith(prefix):
                code_base, idx_base = r, i
                break
    if not code_base: code_base, idx_base = righe[0], 0
    variant = " ".join(righe[idx_base + 1:]).strip()
    variant = re.sub(r'\s+', ' ', variant)
    variant = re.sub(r'-{2,}', '-', variant).strip('-').strip()
    return code_base, variant
