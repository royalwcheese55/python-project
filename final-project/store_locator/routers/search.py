from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session

from ..auth import get_db_session
from ..rate_limit import rate_limiter
from ..schemas import SearchRequest, SearchResponse, StoreResponse
from ..services.geocoding import geocode_address
from ..services.search import search_stores

router = APIRouter(prefix="/api/stores", tags=["stores"])


@router.post("/search", response_model=SearchResponse, dependencies=[Depends(rate_limiter)])
def search_stores_endpoint(
    payload: SearchRequest,
    request: Request,
    session: Session = Depends(get_db_session),
) -> SearchResponse:
    latitude = payload.latitude
    longitude = payload.longitude

    if latitude is None or longitude is None:
        if payload.address:
            coords = geocode_address(payload.address)
        elif payload.postal_code:
            coords = geocode_address(payload.postal_code)
        else:
            coords = None
        if not coords:
            raise HTTPException(status_code=400, detail="Unable to geocode provided location")
        latitude, longitude = coords

    results = search_stores(
        session=session,
        latitude=latitude,
        longitude=longitude,
        radius_miles=payload.radius_miles,
        services=payload.services,
        store_types=payload.store_types,
        open_now=payload.open_now,
    )

    stores = [
        StoreResponse.model_validate(store).model_copy(
            update={"distance_miles": distance, "is_open_now": payload.open_now}
        )
        for store, distance in results
    ]

    return SearchResponse(
        stores=stores,
        metadata={
            "searched_location": {"latitude": latitude, "longitude": longitude},
            "radius_miles": payload.radius_miles,
            "applied_filters": {
                "services": payload.services,
                "store_types": payload.store_types,
                "open_now": payload.open_now,
                "client_ip": request.client.host if request.client else "unknown",
            },
        },
    )
