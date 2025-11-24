from typing import Optional, List, Generator, Annotated

import httpx
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import func
from sqlmodel import (
    SQLModel,
    Field,
    Session,
    create_engine,
    select,
)
from pydantic import BaseModel

# -------------------------------------------------------------------
# Database setup
# -------------------------------------------------------------------

DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    """Provide database session"""
    with Session(engine) as session:
        yield session


# -------------------------------------------------------------------
# Models
# -------------------------------------------------------------------

class UserBase(SQLModel):
    name: str = Field(min_length=1)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class TaskBase(SQLModel):
    title: str = Field(min_length=3)
    content: str = Field(min_length=1)
    city: str = Field(min_length=1)


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")


class TaskCreate(TaskBase):
    user_id: int


class TaskRead(TaskBase):
    id: int
    user_id: int


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=3)
    content: Optional[str] = Field(default=None, min_length=1)
    city: Optional[str] = Field(default=None, min_length=1)
    user_id: Optional[int] = None


# -------------------------------------------------------------------
# Weather models and client
# -------------------------------------------------------------------

class WeatherInfo(BaseModel):
    temperature: float
    windspeed: float
    weathercode: int
    time: str


class TaskWithWeather(TaskRead):
    weather: WeatherInfo


class ForecastClient:
    """Async client to talk to Open-Meteo APIs."""

    def __init__(self, http_client: Optional[httpx.AsyncClient] = None) -> None:
        # Use a shared AsyncClient if provided, otherwise create a new one.
        self.client = http_client or httpx.AsyncClient(timeout=10.0)

    async def get_current_weather(self, city: str) -> WeatherInfo:
        # Step 1: geocoding
        geo_resp = await self.client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json",
            },
        )
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()
        results = geo_data.get("results")

        if not results:
            # City not found as required
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City not found",
            )

        first = results[0]
        lat = first["latitude"]
        lon = first["longitude"]

        # Step 2: weather
        weather_resp = await self.client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
            },
        )
        weather_resp.raise_for_status()
        weather_data = weather_resp.json()
        current = weather_data.get("current_weather")

        if not current:
            # Treat missing current_weather as city not found / unsupported
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City not found",
            )

        return WeatherInfo(**current)


# Reuse one AsyncClient for the whole app
_shared_async_client = httpx.AsyncClient(timeout=10.0)
_forecast_client = ForecastClient(http_client=_shared_async_client)


def get_forecast_client() -> ForecastClient:
    """Provide weather forecast client"""
    return _forecast_client


# -------------------------------------------------------------------
# FastAPI app
# -------------------------------------------------------------------

app = FastAPI(title="Task Management API with Weather")


@app.on_event("startup")
async def on_startup() -> None:
    create_db_and_tables()


# -------------------------------------------------------------------
# User endpoints (CRD)
# -------------------------------------------------------------------

@app.post(
    "/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_in: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    user = User.model_validate(user_in)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users", response_model=List[UserRead])
def list_users(
    db: Annotated[Session, Depends(get_db)],
):
    users = db.exec(select(User)).all()
    return users


@app.get("/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return None


# -------------------------------------------------------------------
# Task endpoints (CRUD)
# -------------------------------------------------------------------

@app.post(
    "/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task_in: TaskCreate,
    db: Annotated[Session, Depends(get_db)],
):
    # Ensure referenced user exists
    user = db.get(User, task_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    task = Task.model_validate(task_in)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.get("/tasks/{task_id}", response_model=TaskWithWeather)
async def get_task(
    task_id: int,
    *,
    db: Annotated[Session, Depends(get_db)],
    forecast_client: Annotated[ForecastClient, Depends(get_forecast_client)],
):
    stmt = select(Task)

    if user_id is not None:
        stmt = stmt.where(Task.user_id == user_id)

    if city is not None:
        # Case-insensitive city filter
        stmt = stmt.where(func.lower(Task.city) == city.lower())

    tasks = db.exec(stmt).all()
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskWithWeather)
async def get_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
    forecast_client: Annotated[ForecastClient, Depends(get_forecast_client)],
):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    weather = await forecast_client.get_current_weather(task.city)

    # Convert ORM object -> Pydantic-friendly dict, then attach weather
    task_data = TaskRead.model_validate(task).model_dump()
    return TaskWithWeather(**task_data, weather=weather)


@app.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # If user_id is being changed, ensure new user exists
    if task_in.user_id is not None:
        user = db.get(User, task_in.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

    update_data = task_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None
