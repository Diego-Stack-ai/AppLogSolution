"""
Geocoding per indirizzi di consegna (600-700 scuole).
- Cache: non ripete richieste per indirizzi già geocodificati
- Salva lat/lon nel file Excel
- Report indirizzi non trovati
"""
import json
import time
from pathlib import Path

import pandas as pd
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from geopy.geocoders import Nominatim

USER_AGENT = "GestioneDDTViaggi-Consegne/1.0"
DELAY_SECONDS = 1.0

# Mappatura nomi colonne (input può usare varianti)
COL_MAP = {
    "indirizzo": ["Indirizzo", "indirizzo", "street"],
    "cap": ["CAP", "cap", "postal_code", "CAP"],
    "citta": ["Città", "Citta", "città", "citta", "city"],
    "provincia": ["Provincia", "provincia", "province"],
    "codice": ["Codice Frutta", "Codice", "codice", "codice_cliente"],
    "nome": ["A chi va consegnato", "Nome", "nome", "nome_cliente", "destinatario"],
}


def _find_column(df: pd.DataFrame, options: list[str]) -> str | None:
    """Trova la prima colonna che esiste nel DataFrame."""
    for opt in options:
        if opt in df.columns:
            return opt
    return None


def _build_address(row: pd.Series, col_indirizzo: str, col_cap: str, col_citta: str, col_prov: str) -> str:
    """Costruisce indirizzo completo normalizzato per cache."""
    def _s(v):
        if pd.isna(v) or v is None: return ""
        s = str(v).strip()
        return "" if s.lower() == "nan" else s
    ind = _s(row.get(col_indirizzo))
    cap_val = row.get(col_cap)
    cap = str(int(cap_val)) if pd.notna(cap_val) and isinstance(cap_val, (int, float)) else _s(cap_val)
    citta = _s(row.get(col_citta))
    prov = _s(row.get(col_prov))
    parts = []
    if ind:
        parts.append(ind)
    if cap or citta:
        loc = f"{cap} {citta}".strip()
        if prov:
            loc = f"{loc} ({prov})"
        parts.append(loc)
    return ", ".join(parts) if parts else ""


def _normalize_for_cache(addr: str) -> str:
    """Normalizza stringa per chiave cache (minuscolo, spazi)."""
    return " ".join(str(addr).lower().split()) if addr else ""


def load_cache(cache_path: Path) -> dict:
    """Carica cache da file JSON."""
    if not cache_path.exists():
        return {}
    try:
        data = json.loads(cache_path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_cache(cache: dict, cache_path: Path) -> None:
    """Salva cache su file JSON."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def geocode_with_cache(
    address: str,
    cache: dict,
    geolocator: Nominatim,
) -> tuple[float | None, float | None, str]:
    """
    Geocodifica un indirizzo. Usa cache se disponibile.
    Ritorna (lat, lon, status) con status: "ok", "not_found", "error"
    """
    key = _normalize_for_cache(address)
    if not key:
        return (None, None, "empty")

    if key in cache:
        c = cache[key]
        return (c.get("lat"), c.get("lon"), c.get("status", "ok"))

    lat, lon = None, None
    status = "not_found"
    try:
        location = geolocator.geocode(address, timeout=10, exactly_one=True)
        if location:
            lat, lon = location.latitude, location.longitude
            status = "ok"
    except (GeocoderTimedOut, GeocoderServiceError):
        status = "error"

    cache[key] = {"lat": lat, "lon": lon, "status": status, "address": address}
    return (lat, lon, status)


def process_excel(
    input_path: Path | str,
    output_path: Path | str | None = None,
    cache_path: Path | str | None = None,
    report_path: Path | str | None = None,
    sheet_name: str | int | None = 0,
) -> dict:
    """
    Legge Excel, geocodifica solo i nuovi indirizzi, salva risultati.
    Ritorna statistiche: {geocoded_new, from_cache, not_found, total_rows}
    """
    input_path = Path(input_path)
    output_path = Path(output_path) if output_path else input_path
    cache_path = Path(cache_path) if cache_path else input_path.parent / "geocode_cache.json"
    report_path = Path(report_path) if report_path else input_path.parent / "geocode_report_non_trovati.xlsx"

    df = pd.read_excel(input_path, sheet_name=sheet_name)

    col_ind = _find_column(df, COL_MAP["indirizzo"])
    col_cap = _find_column(df, COL_MAP["cap"])
    col_citta = _find_column(df, COL_MAP["citta"])
    col_prov = _find_column(df, COL_MAP["provincia"])

    if not all([col_ind, col_cap, col_citta]):
        raise ValueError("Colonne richieste non trovate: Indirizzo, CAP, Città (e opz. Provincia)")

    # Colonne M, N, O per Latitudine, Longitudine, Stato geocoding
    col_lat = "Latitudine"
    col_lon = "Longitudine"
    col_status = "Stato geocoding"
    for c in (col_lat, col_lon, col_status):
        if c not in df.columns:
            df[c] = None
    # Stato geocoding contiene stringhe (ok, not_found, ...): forza dtype object
    df[col_status] = df[col_status].astype(object)
    # Mantieni retrocompatibilità con vecchi nomi
    for old, new in [("latitude", col_lat), ("longitude", col_lon), ("geocode_status", col_status)]:
        if old in df.columns and df[new].isna().all():
            df[new] = df[old]
            df.drop(columns=[old], inplace=True)

    cache = load_cache(cache_path)
    geolocator = Nominatim(user_agent=USER_AGENT)

    stats = {"geocoded_new": 0, "from_cache": 0, "not_found": 0, "total_rows": len(df)}
    not_found_rows = []

    # Raccogli indirizzi unici da processare (per ridurre richieste)
    addr_to_rows: dict[str, list[int]] = {}
    for idx, row in df.iterrows():
        addr = _build_address(row, col_ind, col_cap, col_citta, col_prov or "")
        if addr:
            key = _normalize_for_cache(addr)
            if key not in addr_to_rows:
                addr_to_rows[key] = []
            addr_to_rows[key].append(idx)

    # Processa ogni indirizzo unico
    for key, row_indices in addr_to_rows.items():
        first_idx = row_indices[0]
        row = df.loc[first_idx]

        # Già presente in Excel?
        if pd.notna(df.at[first_idx, col_lat]) and pd.notna(df.at[first_idx, col_lon]):
            for i in row_indices[1:]:
                df.at[i, col_lat] = df.at[first_idx, col_lat]
                df.at[i, col_lon] = df.at[first_idx, col_lon]
                df.at[i, col_status] = "from_excel"
            continue

        addr = _build_address(row, col_ind, col_cap, col_citta, col_prov or "")
        from_cache = key in cache
        lat, lon, status = geocode_with_cache(addr, cache, geolocator)

        for i in row_indices:
            df.at[i, col_lat] = lat
            df.at[i, col_lon] = lon
            df.at[i, col_status] = status

        if status == "ok":
            if from_cache:
                stats["from_cache"] += len(row_indices)
            else:
                stats["geocoded_new"] += len(row_indices)
                time.sleep(DELAY_SECONDS)
        else:
            stats["not_found"] += len(row_indices)
            for i in row_indices:
                not_found_rows.append({
                    "riga": i + 2,
                    "indirizzo": addr,
                    **{c: df.at[i, c] for c in [col_ind, col_cap, col_citta] if c in df.columns},
                })

    save_cache(cache, cache_path)

    # Colonne M, N, O (Excel): Latitudine, Longitudine, Stato geocoding
    df.to_excel(output_path, index=False)

    if not_found_rows:
        pd.DataFrame(not_found_rows).to_excel(report_path, index=False)

    return stats
