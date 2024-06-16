from fastapi import FastAPI

from backend.api.v1.api import api_router
from backend.core.config import settings
from backend.areas.finder import area_finder

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event('startup')
def load_areas_data() -> None:
    area_finder.load_data()
