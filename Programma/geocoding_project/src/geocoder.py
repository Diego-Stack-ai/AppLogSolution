"""
Modulo di geocoding: converte indirizzi in coordinate GPS (lat/lon).
Utilizza Nominatim (OpenStreetMap) tramite geopy.
Progettato per essere facilmente esteso (es. collegamento a database scuole).
"""
import time
from pathlib import Path

import pandas as pd
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from geopy.geocoders import Nominatim

# User-Agent richiesto da Nominatim (inserire email o nome applicazione)
USER_AGENT = "GestioneDDTViaggi-Geocoding/1.0"
DELAY_SECONDS = 1.0


def _build_full_address(row: pd.Series) -> str:
    """
    Costruisce una stringa di indirizzo completa dai campi.
    Formato: via numero, CAP città (provincia)
    """
    parts = []
    street = str(row.get("street", "") or "").strip()
    house = str(row.get("house_number", "") or "").strip()
    if street:
        parts.append(f"{street} {house}".strip())
    cap = str(row.get("postal_code", "") or "").strip()
    city = str(row.get("city", "") or "").strip()
    prov = str(row.get("province", "") or "").strip()
    if cap or city:
        loc = f"{cap} {city}".strip()
        if prov:
            loc = f"{loc} ({prov})"
        parts.append(loc)
    return ", ".join(parts) if parts else ""


def geocode_address(
    address: str,
    geolocator: Nominatim,
) -> tuple[float | None, float | None]:
    """
    Converte un indirizzo in coordinate (lat, lon).
    Ritorna (None, None) se non trovato o in caso di errore.
    """
    if not address or not address.strip():
        return (None, None)
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return (location.latitude, location.longitude)
    except (GeocoderTimedOut, GeocoderServiceError):
        pass
    return (None, None)


def geocode_dataframe(
    df: pd.DataFrame,
    user_agent: str = USER_AGENT,
    delay: float = DELAY_SECONDS,
) -> pd.DataFrame:
    """
    Geocodifica tutte le righe di un DataFrame.
    Richiede colonne: street, house_number, postal_code, city, province.
    Aggiunge full_address, latitude, longitude.
    """
    geolocator = Nominatim(user_agent=user_agent)
    results = []

    for idx, row in df.iterrows():
        full_addr = _build_full_address(row)
        lat, lon = geocode_address(full_addr, geolocator)

        out = {
            "full_address": full_addr,
            "latitude": lat,
            "longitude": lon,
            **{c: row[c] for c in df.columns},
        }
        results.append(out)
        time.sleep(delay)

    return pd.DataFrame(results)


def load_addresses(path: Path | str) -> pd.DataFrame:
    """Carica indirizzi da Excel o CSV."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File non trovato: {path}")

    if path.suffix.lower() in (".xlsx", ".xls"):
        return pd.read_excel(path)
    return pd.read_csv(path, encoding="utf-8")


def save_geocoded(df: pd.DataFrame, path: Path | str) -> None:
    """Salva il risultato in Excel o CSV."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.suffix.lower() in (".xlsx", ".xls"):
        df.to_excel(path, index=False)
    else:
        df.to_csv(path, index=False, encoding="utf-8")
