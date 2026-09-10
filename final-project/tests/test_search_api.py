from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from store_locator.main import app
from store_locator.models import Role, Store, StoreService, User
from store_locator.auth import get_db_session
from store_locator.rate_limit import rate_limiter


@pytest.fixture()
def session(tmp_path) -> Generator[Session, None, None]:
    engine = create_engine(f"sqlite:///{tmp_path/'test.db'}", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seed_data(session)
        yield session


def seed_data(session: Session) -> None:
    role = Role(name="Viewer")
    session.add(role)
    session.commit()
    session.refresh(role)
    user = User(user_id="viewer", email="viewer@test.com", hashed_password="x", role_id=role.id, status="active")
    session.add(user)
    store = Store(
        store_id="S9999",
        name="Test Store",
        store_type="regular",
        status="active",
        latitude=42.0,
        longitude=-71.0,
        address_street="123 Main",
        address_city="Boston",
        address_state="MA",
        address_postal_code="02110",
        address_country="USA",
        phone="617-555-0100",
        services_text="pickup|pharmacy",
        hours_mon="08:00-17:00",
        hours_tue="08:00-17:00",
        hours_wed="08:00-17:00",
        hours_thu="08:00-17:00",
        hours_fri="08:00-17:00",
        hours_sat="09:00-15:00",
        hours_sun="closed",
    )
    session.add(store)
    session.add(StoreService(store_id="S9999", service_name="pickup"))
    session.add(StoreService(store_id="S9999", service_name="pharmacy"))
    session.commit()


@pytest.fixture()
def client(session: Session) -> Generator[TestClient, None, None]:
    def override_db():
        yield session

    app.dependency_overrides[get_db_session] = override_db
    app.dependency_overrides[rate_limiter] = lambda: None
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides = {}


def test_search_by_coordinates(client: TestClient):
    response = client.post(
        "/api/stores/search",
        json={"latitude": 42.0, "longitude": -71.0, "radius_miles": 5, "services": ["pickup"]},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["stores"][0]["store_id"] == "S9999"
