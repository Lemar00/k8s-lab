from fastapi import APIRouter

# Initialize the router
router = APIRouter()

# Readiness probe - checks if the app is ready to accept traffic
@router.get("/health/ready")
async def readiness():
    return {"status": "ready"}

# Liveness probe - checks if the app is still running
@router.get("/health/live")
async def liveness():
    return {"status": "alive"}
