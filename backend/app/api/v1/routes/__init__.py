from fastapi import APIRouter

from .auth import router as auth_router
from .investments import router as investments_router
from .users import router as users_router


router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(investments_router, prefix="/investments", tags=["investments"])
router.include_router(users_router, prefix="/users", tags=["users"])
