from fastapi import APIRouter

router = APIRouter()

@router.get("/up")
async def up():
    return {"status": "Authentication service is up and running!"}
