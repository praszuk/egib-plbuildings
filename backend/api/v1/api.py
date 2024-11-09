from fastapi import APIRouter

from backend.api.v1.buildings import router as buildings_router
from backend.api.v1.area_imports import router as area_imports_router


api_router = APIRouter()
api_router.include_router(buildings_router, prefix='/buildings', tags=['buildings'])
api_router.include_router(area_imports_router, prefix='/area_imports', tags=['area_imports'])
