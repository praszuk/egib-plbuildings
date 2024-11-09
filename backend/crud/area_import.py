from sqlalchemy.orm import Session
from sqlalchemy import select, Sequence

from backend.models.area_import import AreaImport


async def list_latest_area_imports(db: Session) -> Sequence[AreaImport]:
    result = db.execute(
        select(AreaImport)
        .order_by(AreaImport.teryt, AreaImport.id.desc())
        .distinct(AreaImport.teryt)
    )
    return result.scalars().all()
