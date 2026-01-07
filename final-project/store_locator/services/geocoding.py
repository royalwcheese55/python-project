from __future__ import annotations

from typing import Optional, Tuple

import requests

from ..config import settings
from .cache import TTLCache

_geocode_cache = TTLCache()
_THIRTY_DAYS_SECONDS = 60 * 60 * 24 * 30
_NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    cached = _geocode_cache.get(address)
    if cached:
        return cached

    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": settings.geocoding_user_agent}
    response = requests.get(_NOMINATIM_URL, params=params, headers=headers, timeout=10)
    if response.status_code != 200:
        return None
    data = response.json()
    if not data:
        return None
    first = data[0]
    coords = (float(first["lat"]), float(first["lon"]))
    _geocode_cache.set(address, coords, _THIRTY_DAYS_SECONDS)
    return coords
