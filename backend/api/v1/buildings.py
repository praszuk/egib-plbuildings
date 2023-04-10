from fastapi import APIRouter, Depends

from typing import Any, Dict, Optional

from backend.api.v1.deps import Location
from backend.services import buildings


router = APIRouter()


@router.get('/')
async def get_building_at(
    location: Location = Depends(Location),
) -> Optional[Dict[str, Any]]:
    return await buildings.get_building_at(location.lat, location.lon)
