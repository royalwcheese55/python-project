import csv
import os
from datetime import datetime, timedelta, timezone
from typing import Iterable, List, Optional

from sqlmodel import Session, select

from .auth import hash_password
from .models import Permission, RefreshToken, Role, RolePermission, Store, StoreService, User
from .services.hours import validate_hours

DEFAULT_USERS = [
    ("admin", "admin@test.com", "Admin", "AdminTest123!"),
    ("marketer", "marketer@test.com", "Marketer", "MarketerTest123!"),
    ("viewer", "viewer@test.com", "Viewer", "ViewerTest123!"),
]

DEFAULT_PERMISSIONS = {
    "Admin": ["stores:read", "stores:write", "users:manage"],
    "Marketer": ["stores:read", "stores:write"],
    "Viewer": ["stores:read"],
}


def ensure_roles_and_permissions(session: Session) -> None:
    role_cache = {}
    for role_name, permissions in DEFAULT_PERMISSIONS.items():
        role = session.exec(select(Role).where(Role.name == role_name)).first()
        if not role:
            role = Role(name=role_name, description=f"{role_name} role")
            session.add(role)
            session.commit()
            session.refresh(role)
        role_cache[role_name] = role
        for perm_name in permissions:
            permission = session.exec(select(Permission).where(Permission.name == perm_name)).first()
            if not permission:
                permission = Permission(name=perm_name, description=f"{perm_name} permission")
                session.add(permission)
                session.commit()
                session.refresh(permission)
            link = session.exec(
                select(RolePermission).where(
                    RolePermission.role_id == role.id, RolePermission.permission_id == permission.id
                )
            ).first()
            if not link:
                session.add(RolePermission(role_id=role.id, permission_id=permission.id))
                session.commit()
    session.expire_all()


def ensure_default_users(session: Session) -> None:
    role_map = {role.name: role for role in session.exec(select(Role)).all()}
    for user_id, email, role_name, password in DEFAULT_USERS:
        existing = session.exec(select(User).where(User.email == email)).first()
        if existing:
            continue
        role = role_map.get(role_name)
        if not role:
            continue
        user = User(
            user_id=user_id,
            email=email,
            hashed_password=hash_password(password),
            role_id=role.id,
            status="active",
        )
        session.add(user)
        session.commit()


def _parse_services(value: str) -> List[str]:
    return [item for item in value.split("|") if item]


def _validated_hours(row: dict) -> bool:
    return all(validate_hours(row[f"hours_{day}"]) for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"])


def seed_stores_from_csv(session: Session, csv_path: str, limit: Optional[int] = None) -> int:
    if not os.path.exists(csv_path):
        return 0
    inserted = 0
    with open(csv_path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for idx, row in enumerate(reader):
            if limit and idx >= limit:
                break
            if session.exec(select(Store).where(Store.store_id == row["store_id"])).first():
                continue
            if not _validated_hours(row):
                continue
            store = Store(
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
                services_text=row["services"],
                hours_mon=row["hours_mon"],
                hours_tue=row["hours_tue"],
                hours_wed=row["hours_wed"],
                hours_thu=row["hours_thu"],
                hours_fri=row["hours_fri"],
                hours_sat=row["hours_sat"],
                hours_sun=row["hours_sun"],
            )
            session.add(store)
            for service in _parse_services(row["services"]):
                session.add(StoreService(store_id=store.store_id, service_name=service))
            inserted += 1
        session.commit()
    return inserted


def initialize_database(session: Session, base_path: str) -> None:
    ensure_roles_and_permissions(session)
    ensure_default_users(session)
    seed_stores_from_csv(session, os.path.join(base_path, "stores_50.csv"), limit=50)
