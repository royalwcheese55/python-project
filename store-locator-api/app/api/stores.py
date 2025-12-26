from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.deps import get_current_user
from app.models.user import User

from app.db.deps import get_db
from app.schemas.store_search import StoreSearchRequest, StoreSearchResponse, StoreResult
from app.services.store_search import search_stores

router = APIRouter(prefix="/api/stores", tags=["Stores"])

@router.post("/search", response_model=StoreSearchResponse)
def store_search(
    payload: StoreSearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 👈 this line
):
    rows = search_stores(
        db=db,
        lat=payload.lat,
        lon=payload.lon,
        radius_miles=payload.radius_miles,
        services=payload.services,
        store_types=payload.store_types,
        open_now=payload.open_now,
    )

    results = []
    for dist, s, open_flag in rows:
        results.append(StoreResult(
            store_id=s.store_id,
            name=s.name,
            store_type=s.store_type,
            status=s.status,
            latitude=s.latitude,
            longitude=s.longitude,
            address_street=s.address_street,
            address_city=s.address_city,
            address_state=s.address_state,
            address_postal_code=s.address_postal_code,
            address_country=s.address_country,
            phone=s.phone,
            services=s.services,
            is_open_now=open_flag,
            distance_miles=round(dist, 3),
        ))
    total = len(results)
    paged_results = results[payload.offset : payload.offset + payload.limit]

    return StoreSearchResponse(
    location={"lat": payload.lat, "lon": payload.lon},
    applied_filters={
        "radius_miles": payload.radius_miles,
        "services": payload.services or [],
        "store_types": payload.store_types or [],
        "open_now": payload.open_now,
    },
    total=total,
    limit=payload.limit,
    offset=payload.offset,
    results=paged_results,
)
