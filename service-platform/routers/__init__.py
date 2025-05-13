from fastapi import APIRouter
from . import songchord
router = APIRouter()

router.include_router(
    songchord.router,
    tags=["songchord"],
    prefix="/songchord",
)
