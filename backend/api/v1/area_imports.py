from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.areas.config import all_areas
from backend.models.area_import import AreaImport as AreaImportModel
from backend.database.session import get_db
from backend.crud.area_import import list_latest_area_imports, list_stable_area_imports
from backend.schemas.area_import import AreaImport as AreaImportSchema

router = APIRouter()


def convert_to_area_import_schema(db_area_import: AreaImportModel) -> AreaImportSchema:
    return AreaImportSchema(
        id=db_area_import.id,
        name=all_areas[db_area_import.teryt].name,
        teryt=db_area_import.teryt,
        start_at=db_area_import.start_at,
        end_at=db_area_import.end_at,
        result_status=db_area_import.result_status,
        building_count=db_area_import.building_count,
        has_building_type=db_area_import.has_building_type,
        has_building_levels=db_area_import.has_building_levels,
        has_building_levels_undg=db_area_import.has_building_levels_undg,
        data_check_has_expected_tags=db_area_import.data_check_has_expected_tags,  # noqa
        data_check_expected_tags=db_area_import.data_check_expected_tags,
        data_check_result_tags=db_area_import.data_check_result_tags,
    )


@router.get('/latest')
async def get_latest_area_imports(db: Session = Depends(get_db)) -> list[AreaImportSchema]:
    db_latest_area_imports = await list_latest_area_imports(db)
    return [
        convert_to_area_import_schema(db_area_import)
        for db_area_import in db_latest_area_imports  # noqa
    ]


@router.get('/stable')
async def get_stable_area_imports(db: Session = Depends(get_db)) -> list[AreaImportSchema]:
    db_stable_area_imports = await list_stable_area_imports(db)
    return [
        convert_to_area_import_schema(db_area_import)
        for db_area_import in db_stable_area_imports  # noqa
    ]
