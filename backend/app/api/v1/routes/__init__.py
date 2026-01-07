from fastapi import APIRouter


router = APIRouter()

@router.get("/health", tags=["health"])
async def up():
    return {"status": "API service is up and running!"}

@router.get("/version", tags=["health"])
async def get_version():
    return {"version": "1.0.0"}
