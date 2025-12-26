from fastapi import FastAPI
from app.api.stores import router as stores_router
from app.api.auth import router as auth_router

app = FastAPI(title="Store Locator API")

app.include_router(stores_router)
app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}