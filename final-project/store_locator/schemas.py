from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from .services.hours import validate_hours


class StoreBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    store_id: str = Field(..., pattern=r"^S\d{4}$")
    name: str
    store_type: str
    status: str = "active"
    latitude: float
    longitude: float
    address_street: str
    address_city: str
    address_state: str
    address_postal_code: str
    address_country: str
    phone: str
    services: List[str]
    hours_mon: str
    hours_tue: str
    hours_wed: str
    hours_thu: str
    hours_fri: str
    hours_sat: str
    hours_sun: str

    @field_validator(
        "hours_mon",
        "hours_tue",
        "hours_wed",
        "hours_thu",
        "hours_fri",
        "hours_sat",
        "hours_sun",
    )
    @classmethod
    def validate_hours_format(cls, v: str) -> str:
        if not validate_hours(v):
            raise ValueError("Invalid hours format")
        return v


class StoreCreate(StoreBase):
    pass


class StoreUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    services: Optional[List[str]] = None
    status: Optional[str] = None
    hours_mon: Optional[str] = None
    hours_tue: Optional[str] = None
    hours_wed: Optional[str] = None
    hours_thu: Optional[str] = None
    hours_fri: Optional[str] = None
    hours_sat: Optional[str] = None
    hours_sun: Optional[str] = None

    @field_validator(
        "hours_mon",
        "hours_tue",
        "hours_wed",
        "hours_thu",
        "hours_fri",
        "hours_sat",
        "hours_sun",
    )
    @classmethod
    def validate_hours_if_present(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not validate_hours(v):
            raise ValueError("Invalid hours format")
        return v


class StoreResponse(StoreBase):
    distance_miles: Optional[float] = None
    is_open_now: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class SearchRequest(BaseModel):
    address: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_miles: float = Field(default=10, gt=0, le=100)
    services: List[str] = Field(default_factory=list)
    store_types: List[str] = Field(default_factory=list)
    open_now: bool = False


class SearchMetadata(BaseModel):
    searched_location: dict
    radius_miles: float
    applied_filters: dict


class SearchResponse(BaseModel):
    stores: List[StoreResponse]
    metadata: SearchMetadata


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class UserCreate(BaseModel):
    user_id: str
    email: EmailStr
    password: str
    role: str


class UserResponse(BaseModel):
    user_id: str
    email: EmailStr
    role: str
    status: str

    model_config = ConfigDict(from_attributes=True)
