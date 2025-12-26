import math
from datetime import datetime
from geopy.distance import geodesic
from app.models.store import Store
from app.core.geo import bounding_box, haversine_miles

def bounding_box(lat: float, lon: float, radius_miles: float):
    lat_delta = radius_miles / 69.0
    lon_delta = radius_miles / (69.0 * math.cos(math.radians(lat)))
    return (
        lat - lat_delta,
        lat + lat_delta,
        lon - lon_delta,
        lon + lon_delta,
    )

def parse_services(services_str: str | None) -> set[str]:
    if not services_str:
        return set()
    return set(services_str.split("|"))

def is_open_now_for_store(store: Store, now: datetime) -> bool:
    # Basic version: uses weekday hours string like "08:00-22:00" or "closed"
    weekday = now.weekday()  # Mon=0 ... Sun=6
    field = ["hours_mon","hours_tue","hours_wed","hours_thu","hours_fri","hours_sat","hours_sun"][weekday]
    hours = getattr(store, field)

    if not hours or hours == "closed":
        return False

    open_str, close_str = hours.split("-")
    open_h, open_m = map(int, open_str.split(":"))
    close_h, close_m = map(int, close_str.split(":"))

    open_minutes = open_h * 60 + open_m
    close_minutes = close_h * 60 + close_m
    now_minutes = now.hour * 60 + now.minute

    return open_minutes <= now_minutes < close_minutes

def search_stores(db, lat: float, lon: float, radius_miles: float, services=None, store_types=None, open_now=None):
    min_lat, max_lat, min_lon, max_lon = bounding_box(lat, lon, radius_miles)

    q = db.query(Store).filter(
        Store.status == "active",
        Store.latitude.between(min_lat, max_lat),
        Store.longitude.between(min_lon, max_lon),
    )

    if store_types:
        q = q.filter(Store.store_type.in_(store_types))

    candidates = q.all()

    now = datetime.now()
    results = []

    required_services = set(services or [])

    for s in candidates:
        dist = haversine_miles(lat, lon, s.latitude, s.longitude)
        if dist > radius_miles:
            continue

        store_services = parse_services(s.services)
        # services AND logic
        if required_services and not required_services.issubset(store_services):
            continue

        open_flag = is_open_now_for_store(s, now)
        if open_now is True and not open_flag:
            continue

        results.append((dist, s, open_flag))

    results.sort(key=lambda x: x[0])

    return results