from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .bootstrap import initialize_database
from .database import init_db, session_scope
from .routers import admin, search

BASE_PATH = Path(__file__).resolve().parent.parent

app = FastAPI(title="Store Locator Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    init_db()
    with session_scope() as session:
        initialize_database(session, base_path=str(BASE_PATH))


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok"}


app.include_router(search.router)
app.include_router(admin.router)
