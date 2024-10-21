from typing import Any, Dict

from fastapi import APIRouter, Depends

from backend.api.v1.deps import Location
from backend.services import buildings

router = APIRouter()


@router.get('/')
async def get_building_at(
    location: Location = Depends(Location),
    live: bool = False,
) -> Dict[str, Any]:
    if not live:
        return await buildings.query_building_from_db_at(location.lat, location.lon)

    return await buildings.get_building_live_at(location.lat, location.lon)
