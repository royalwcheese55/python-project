import csv
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlmodel import Session, delete, select

from ..auth import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_db_session,
    hash_password,
    hash_refresh_token,
    require_role,
    revoke_refresh_token,
    verify_password,
)
from ..config import refresh_token_timedelta, settings
from ..models import RefreshToken, Role, Store, StoreService, User
from ..schemas import (
    LoginRequest,
    RefreshRequest,
    StoreCreate,
    StoreResponse,
    StoreUpdate,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from ..services.geocoding import geocode_address
from ..services.hours import validate_hours

router = APIRouter(prefix="/api/admin", tags=["admin"])


def _persist_store(session: Session, store_data: StoreCreate) -> Store:
    store = Store(**store_data.dict(exclude={"services"}), services_text="|".join(store_data.services))
    session.add(store)
    for service in store_data.services:
        session.add(StoreService(store_id=store.store_id, service_name=service))
    session.commit()
    session.refresh(store)
    return store


@router.post("/stores", response_model=StoreResponse)
def create_store(
    store: StoreCreate,
    session: Session = Depends(get_db_session),
    current_user=Depends(require_role("Admin", "Marketer")),
) -> StoreResponse:
    if session.exec(select(Store).where(Store.store_id == store.store_id)).first():
        raise HTTPException(status_code=400, detail="Store already exists")
    if (not store.latitude or not store.longitude) and store.address_postal_code:
        address = f"{store.address_street}, {store.address_city}, {store.address_state} {store.address_postal_code}"
        coords = geocode_address(address)
        if coords:
            store.latitude, store.longitude = coords
    db_store = _persist_store(session, store)
    return StoreResponse.from_orm(db_store)


@router.get("/stores", response_model=List[StoreResponse])
def list_stores(
    offset: int = 0,
    limit: int = 20,
    session: Session = Depends(get_db_session),
    current_user=Depends(require_role("Admin", "Marketer", "Viewer")),
) -> List[StoreResponse]:
    stores = session.exec(select(Store).offset(offset).limit(limit)).all()
    return [StoreResponse.from_orm(s) for s in stores]


@router.get("/stores/{store_id}", response_model=StoreResponse)
def get_store(
    store_id: str,
    session: Session = Depends(get_db_session),
    current_user=Depends(require_role("Admin", "Marketer", "Viewer")),
) -> StoreResponse:
    store = session.exec(select(Store).where(Store.store_id == store_id)).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return StoreResponse.from_orm(store)


@router.patch("/stores/{store_id}", response_model=StoreResponse)
def update_store(
    store_id: str,
    payload: StoreUpdate,
    session: Session = Depends(get_db_session),
    current_user=Depends(require_role("Admin", "Marketer")),
) -> StoreResponse:
    store = session.exec(select(Store).where(Store.store_id == store_id)).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    for field, value in payload.dict(exclude_unset=True).items():
        if field == "services" and value is not None:
            session.exec(delete(StoreService).where(StoreService.store_id == store_id))
            for service in value:
                session.add(StoreService(store_id=store_id, service_name=service))
            store.services_text = "|".join(value)
            continue
        if value is not None:
            setattr(store, field, value)
    session.add(store)
    session.commit()
    session.refresh(store)
    return StoreResponse.from_orm(store)


@router.delete("/stores/{store_id}", status_code=204)
def deactivate_store(
    store_id: str,
    session: Session = Depends(get_db_session),
    current_user=Depends(require_role("Admin", "Marketer")),
) -> None:
    store = session.exec(select(Store).where(Store.store_id == store_id)).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    store.status = "inactive"
    session.add(store)
    session.commit()


@router.post("/stores/import", response_model=dict)
async def import_stores(
    file: UploadFile = File(...),
    session: Session = Depends(get_db_session),
    current_user=Depends(require_role("Admin", "Marketer")),
) -> dict:
    contents = await file.read()
    text = contents.decode("utf-8").splitlines()
    reader = csv.DictReader(text)
    expected_headers = [
        "store_id",
        "name",
        "store_type",
        "status",
        "latitude",
        "longitude",
        "address_street",
        "address_city",
        "address_state",
        "address_postal_code",
        "address_country",
        "phone",
        "services",
        "hours_mon",
        "hours_tue",
        "hours_wed",
        "hours_thu",
        "hours_fri",
        "hours_sat",
        "hours_sun",
    ]
    if reader.fieldnames != expected_headers:
        raise HTTPException(status_code=400, detail="CSV headers do not match required format")
    created = updated = failed = 0
    errors: List[str] = []
    for idx, row in enumerate(reader, start=2):
        if not _row_valid(row):
            failed += 1
            errors.append(f"Row {idx}: validation failed")
            continue
        store_data = StoreCreate(
            store_id=row["store_id"],
            name=row["name"],
            store_type=row["store_type"],
            status=row["status"],
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            address_street=row["address_street"],
            address_city=row["address_city"],
            address_state=row["address_state"],
            address_postal_code=row["address_postal_code"],
            address_country=row["address_country"],
            phone=row["phone"],
            services=row["services"].split("|"),
            hours_mon=row["hours_mon"],
            hours_tue=row["hours_tue"],
            hours_wed=row["hours_wed"],
            hours_thu=row["hours_thu"],
            hours_fri=row["hours_fri"],
            hours_sat=row["hours_sat"],
            hours_sun=row["hours_sun"],
        )
        existing = session.exec(select(Store).where(Store.store_id == store_data.store_id)).first()
        if existing:
            for field, value in store_data.dict().items():
                if field == "services":
                    session.exec(delete(StoreService).where(StoreService.store_id == existing.store_id))
                    for service in value:
                        session.add(StoreService(store_id=existing.store_id, service_name=service))
                    existing.services_text = "|".join(value)
                    continue
                setattr(existing, field, value)
            updated += 1
            session.add(existing)
        else:
            _persist_store(session, store_data)
            created += 1
    session.commit()
    return {"created": created, "updated": updated, "failed": failed, "errors": errors}


def _row_valid(row: dict) -> bool:
    try:
        float(row["latitude"])
        float(row["longitude"])
    except ValueError:
        return False
    return _validated_hours(row)


def _validated_hours(row: dict) -> bool:
    for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
        if not validate_hours(row[f"hours_{day}"]):
            return False
    return True


@router.post("/users", response_model=UserResponse)
def create_user(
    payload: UserCreate,
    session: Session = Depends(get_db_session),
    current_user=Depends(require_role("Admin")),
) -> UserResponse:
    if session.exec(select(User).where(User.email == payload.email)).first():
        raise HTTPException(status_code=400, detail="User already exists")
    role = session.exec(select(Role).where(Role.name == payload.role)).first()
    if not role:
        raise HTTPException(status_code=400, detail="Role not found")
    user = User(
        user_id=payload.user_id,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role_id=role.id,
        status="active",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserResponse(user_id=user.user_id, email=user.email, role=role.name, status=user.status)


@router.get("/users", response_model=List[UserResponse])
def list_users(
    session: Session = Depends(get_db_session), current_user=Depends(require_role("Admin"))
) -> List[UserResponse]:
    users = session.exec(select(User)).all()
    return [
        UserResponse(
            user_id=user.user_id,
            email=user.email,
            role=user.role.name if user.role else "unknown",
            status=user.status,
        )
        for user in users
    ]


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    role: Optional[str] = None,
    status_value: Optional[str] = None,
    session: Session = Depends(get_db_session),
    current_user=Depends(require_role("Admin")),
) -> UserResponse:
    user = session.exec(select(User).where(User.user_id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if role:
        role_obj = session.exec(select(Role).where(Role.name == role)).first()
        if not role_obj:
            raise HTTPException(status_code=400, detail="Role not found")
        user.role_id = role_obj.id
    if status_value:
        user.status = status_value
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserResponse(
        user_id=user.user_id, email=user.email, role=user.role.name if user.role else "unknown", status=user.status
    )


@router.delete("/users/{user_id}", status_code=204)
def deactivate_user(
    user_id: str,
    session: Session = Depends(get_db_session),
    current_user=Depends(require_role("Admin")),
) -> None:
    user = session.exec(select(User).where(User.user_id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = "inactive"
    session.add(user)
    session.commit()


# Authentication endpoints
@router.post("/auth/login", response_model=TokenResponse, tags=["auth"])
def login(payload: LoginRequest, session: Session = Depends(get_db_session)) -> TokenResponse:
    user = session.exec(select(User).where(User.email == payload.email)).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"user_id": user.user_id, "email": user.email, "role": user.role.name})
    refresh_token = create_refresh_token({"user_id": user.user_id, "email": user.email, "role": user.role.name})
    token_hash = hash_refresh_token(refresh_token)
    expires_at = datetime.now(tz=timezone.utc) + refresh_token_timedelta()
    session.add(RefreshToken(user_id=user.id, token_hash=token_hash, expires_at=expires_at, revoked=False))
    session.commit()
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/auth/refresh", response_model=TokenResponse, tags=["auth"])
def refresh(payload: RefreshRequest, session: Session = Depends(get_db_session)) -> TokenResponse:
    token_hash = hash_refresh_token(payload.refresh_token)
    record = session.exec(select(RefreshToken).where(RefreshToken.token_hash == token_hash)).first()
    if not record or record.revoked or record.expires_at < datetime.now(tz=timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user = session.get(User, record.user_id)
    access_token = create_access_token({"user_id": user.user_id, "email": user.email, "role": user.role.name})
    return TokenResponse(access_token=access_token, refresh_token=payload.refresh_token)


@router.post("/auth/logout", status_code=204, tags=["auth"])
def logout(payload: RefreshRequest, session: Session = Depends(get_db_session)) -> None:
    revoke_refresh_token(session, payload.refresh_token)
