from sqlalchemy.orm import Session
from sqlalchemy import case, func, select, Sequence

from backend.models.area_import import AreaImport
from backend.models.area_import import ResultStatus


async def list_latest_area_imports(db: Session) -> Sequence[AreaImport]:
    result = db.execute(
        select(AreaImport)
        .order_by(AreaImport.teryt, AreaImport.id.desc())
        .distinct(AreaImport.teryt)
    )
    return result.scalars().all()


async def list_stable_area_imports(db: Session) -> Sequence[AreaImport]:
    # noinspection PyTypeChecker
    ranked_areas_subquery = select(
        AreaImport,
        func.row_number()
        .over(
            partition_by=AreaImport.teryt,
            order_by=(
                case((AreaImport.result_status == ResultStatus.SUCCESS, 1), else_=2),
                AreaImport.id.desc(),
            ),
        )
        .label('rank'),
    ).subquery()
    # noinspection PyTypeChecker
    stmt = (
        select(ranked_areas_subquery)
        .where(ranked_areas_subquery.c.rank == 1)
        .order_by(ranked_areas_subquery.c.teryt)
    )
    result = db.execute(select(AreaImport).from_statement(stmt))
    return result.scalars().all()
