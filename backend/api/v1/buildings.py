from fastapi import APIRouter, Depends

from backend.services import buildings

from backend.api.v1.deps import Location


router = APIRouter()


@router.get('/')
async def get_building_at(location=Depends(Location)):
    return await buildings.get_building_at(location.lat, location.lon)
