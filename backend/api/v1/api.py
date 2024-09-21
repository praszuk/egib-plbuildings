from fastapi import APIRouter

from backend.api.v1.buildings import router as buildings_router

api_router = APIRouter()
api_router.include_router(buildings_router, prefix='/buildings', tags=['buildings'])
