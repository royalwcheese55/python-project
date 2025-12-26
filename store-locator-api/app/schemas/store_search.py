from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class StoreSearchRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)

    radius_miles: float = Field(10, gt=0, le=100)
    services: Optional[List[str]] = None
    store_types: Optional[List[Literal["flagship","regular","outlet","express"]]] = None
    open_now: Optional[bool] = None
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)

class StoreResult(BaseModel):
    store_id: str
    name: str
    store_type: str
    status: str
    latitude: float
    longitude: float
    address_street: str
    address_city: str
    address_state: str
    address_postal_code: str
    address_country: str
    phone: Optional[str]
    services: Optional[str]
    is_open_now: bool
    distance_miles: float

class StoreSearchResponse(BaseModel):
    location: dict
    applied_filters: dict
    total: int
    limit: int
    offset: int
    results: List[StoreResult]
