from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple

from sqlmodel import Session, select

from ..models import Store, StoreService
from .cache import TTLCache
from .hours import is_open_now

SEARCH_CACHE = TTLCache()
SEARCH_CACHE_TTL_SECONDS = 600


@dataclass
class BoundingBox:
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float


def calculate_bounding_box(latitude: float, longitude: float, radius_miles: float) -> BoundingBox:
    latitude_delta = radius_miles / 69.0
    longitude_delta = radius_miles / (69.0 * math.cos(math.radians(latitude)))
    return BoundingBox(
        min_lat=latitude - latitude_delta,
        max_lat=latitude + latitude_delta,
        min_lon=longitude - longitude_delta,
        max_lon=longitude + longitude_delta,
    )


def _filter_by_services(session: Session, services: List[str]) -> List[str]:
    if not services:
        return []
    store_ids = None
    for service in services:
        ids = set(
            session.exec(
                select(StoreService.store_id).where(StoreService.service_name == service)
            ).all()
        )
        store_ids = ids if store_ids is None else store_ids.intersection(ids)
    return list(store_ids or [])


def search_stores(
    session: Session,
    latitude: float,
    longitude: float,
    radius_miles: float,
    services: List[str],
    store_types: List[str],
    open_now: bool,
) -> List[Tuple[Store, float]]:
    cache_key = f"{latitude}:{longitude}:{radius_miles}:{'|'.join(sorted(services))}:{'|'.join(sorted(store_types))}:{open_now}"
    cached = SEARCH_CACHE.get(cache_key)
    if cached:
        return cached

    box = calculate_bounding_box(latitude, longitude, radius_miles)
    statement = (
        select(Store)
        .where(Store.latitude.between(box.min_lat, box.max_lat))
        .where(Store.longitude.between(box.min_lon, box.max_lon))
        .where(Store.status == "active")
    )
    if store_types:
        statement = statement.where(Store.store_type.in_(store_types))

    stores = session.exec(statement).all()

    if services:
        allowed_ids = set(_filter_by_services(session, services))
        stores = [s for s in stores if s.store_id in allowed_ids]

    enriched: List[Tuple[Store, float]] = []
    for store in stores:
        distance = haversine_distance_miles((latitude, longitude), (store.latitude, store.longitude))
        if distance <= radius_miles:
            if open_now:
                day_name = _current_day_name()
                hours_value = getattr(store, f"hours_{day_name}")
                if not is_open_now(hours_value):
                    continue
            enriched.append((store, distance))

    enriched.sort(key=lambda item: item[1])
    SEARCH_CACHE.set(cache_key, enriched, SEARCH_CACHE_TTL_SECONDS)
    return enriched


def _current_day_name() -> str:
    from datetime import datetime

    return ["mon", "tue", "wed", "thu", "fri", "sat", "sun"][datetime.utcnow().weekday()]


def haversine_distance_miles(origin: Tuple[float, float], destination: Tuple[float, float]) -> float:
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius_miles = 3959

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_miles * c
