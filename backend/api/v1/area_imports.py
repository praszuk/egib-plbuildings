from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.crud.area_import import list_latest_area_imports, list_stable_area_imports

router = APIRouter()


@router.get('/latest')
async def get_latest_area_imports(db: Session = Depends(get_db)):
    return await list_latest_area_imports(db)


@router.get('/stable')
async def get_stable_area_imports(db: Session = Depends(get_db)):
    return await list_stable_area_imports(db)
