from fastapi import FastAPI
from app.routers import upload, records

app = FastAPI(title="Test Job Service")

app.include_router(upload.router)
app.include_router(records.router)
