from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.api.v1.deps import Location
from backend.crud import building
from backend.database.session import get_db


router = APIRouter()


@router.get('/')
async def get_building_at(
    location: Location = Depends(Location), db: Session = Depends(get_db)
) -> Dict[str, Any]:
    return await building.get_building_at(db, location.lat, location.lon)
