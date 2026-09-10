from datetime import datetime
from typing import List, Optional

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, String


class StoreService(SQLModel, table=True):
    store_id: str = Field(foreign_key="store.store_id", primary_key=True)
    service_name: str = Field(primary_key=True)

    store: Optional["Store"] = Relationship(back_populates="service_links")


class Store(SQLModel, table=True):
    store_id: str = Field(primary_key=True, index=True)
    name: str
    store_type: str = Field(index=True)
    status: str = Field(default="active", index=True)
    latitude: float = Field(index=True)
    longitude: float = Field(index=True)
    address_street: str
    address_city: str
    address_state: str = Field(max_length=2)
    address_postal_code: str = Field(max_length=5, index=True)
    address_country: str = Field(max_length=3, default="USA")
    phone: str
    services_text: Optional[str] = None
    hours_mon: str
    hours_tue: str
    hours_wed: str
    hours_thu: str
    hours_fri: str
    hours_sat: str
    hours_sun: str

    service_links: List[StoreService] = Relationship(back_populates="store")

    @property
    def services(self) -> List[str]:
        if self.service_links:
            return sorted(link.service_name for link in self.service_links)
        if self.services_text:
            return self.services_text.split("|")
        return []


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None

    users: List["User"] = Relationship(back_populates="role")
    permissions: List["RolePermission"] = Relationship(back_populates="role")


class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None

    roles: List["RolePermission"] = Relationship(back_populates="permission")


class RolePermission(SQLModel, table=True):
    role_id: int = Field(foreign_key="role.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)

    role: Optional[Role] = Relationship(back_populates="permissions")
    permission: Optional[Permission] = Relationship(back_populates="roles")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    role_id: int = Field(foreign_key="role.id")
    status: str = Field(default="active")

    role: Optional[Role] = Relationship(back_populates="users")
    refresh_tokens: List["RefreshToken"] = Relationship(back_populates="user")


class RefreshToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token_hash: str = Field(sa_column=Column(String, unique=True, index=True))
    expires_at: datetime
    revoked: bool = Field(default=False)

    user: Optional[User] = Relationship(back_populates="refresh_tokens")
