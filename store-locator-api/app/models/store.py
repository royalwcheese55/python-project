from sqlalchemy import (
    Column,
    String,
    Float,
    Enum,
    Index
)
from app.db.database import Base

# Enums from project spec
StoreTypeEnum = Enum(
    "flagship",
    "regular",
    "outlet",
    "express",
    name="store_type_enum"
)

StoreStatusEnum = Enum(
    "active",
    "inactive",
    "temporarily_closed",
    name="store_status_enum"
)


class Store(Base):
    __tablename__ = "stores"

    # Core identity
    store_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Classification
    store_type = Column(StoreTypeEnum, nullable=False)
    status = Column(StoreStatusEnum, nullable=False, default="active")

    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Address
    address_street = Column(String, nullable=False)
    address_city = Column(String, nullable=False)
    address_state = Column(String(2), nullable=False)
    address_postal_code = Column(String(5), nullable=False)
    address_country = Column(String(3), nullable=False)

    # Contact
    phone = Column(String, nullable=True)

    # Services (pipe-separated for now, normalized later)
    services = Column(String, nullable=True)

    # Hours
    hours_mon = Column(String, nullable=False)
    hours_tue = Column(String, nullable=False)
    hours_wed = Column(String, nullable=False)
    hours_thu = Column(String, nullable=False)
    hours_fri = Column(String, nullable=False)
    hours_sat = Column(String, nullable=False)
    hours_sun = Column(String, nullable=False)

    __table_args__ = (
        # Required indexes
        Index("idx_store_lat_lon", "latitude", "longitude"),
        Index("idx_store_status", "status"),
        Index("idx_store_type", "store_type"),
        Index("idx_store_postal", "address_postal_code"),
    )