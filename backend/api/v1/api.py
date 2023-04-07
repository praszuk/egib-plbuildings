from fastapi import APIRouter

from .buildings import router as buildings_router


api_router = APIRouter()
api_router.include_router(
    buildings_router,
    prefix='/buildings',
    tags=['buildings']
)
