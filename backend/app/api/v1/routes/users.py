from fastapi import APIRouter

router = APIRouter()

@router.get("/up")
async def up():
    return {"status": "User service is up and running!"}
