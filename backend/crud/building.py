from typing import Any, Dict

from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.orm import Session

from backend.models.building import Building


async def get_building_at(db: Session, lat: float, lon: float) -> Dict[str, Any]:
    # fmt: off
    query = (
        select(
            func.json_build_object(
                'type', 'Feature',
                'geometry', Building.geometry,
                'properties', Building.tags
            )
        )
        .where(
            func.ST_Contains(Building.geometry, func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326))
        )
        .limit(1)
    )
    #  fmt: on

    result = {'type': 'FeatureCollection', 'features': []}
    if feature := db.execute(query).scalar():
        result['features'].append(feature)

    return result
