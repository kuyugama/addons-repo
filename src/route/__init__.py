from fastapi import APIRouter

router = APIRouter()

__all__ = ["router"]

from .auth import router as auth_router
from .addon import router as addon_router

router.include_router(auth_router, tags=["Authorization"])
router.include_router(addon_router, tags=["Addons"])
