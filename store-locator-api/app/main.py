from fastapi import FastAPI
from app.api.stores import router as stores_router

app = FastAPI(title="Store Locator API")

app.include_router(stores_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}