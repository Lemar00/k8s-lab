from fastapi import FastAPI
from app.server.routers import health, items
from app.server.database import init_db

# Initialize FastAPI application
app = FastAPI(title="Python Kubernetes Lab API", version="1.0")

# Event to initialize the database on application startup
@app.on_event("startup")
async def on_startup():
    await init_db()

# Registering routers for modular route management
app.include_router(health.router, prefix="/health", tags=["Health Check"])
app.include_router(items.router, prefix="/items", tags=["Items"])

# Root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "HELLO, welcome to my Python Kubernetes Lab!"}
