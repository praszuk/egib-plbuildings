from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from backend.api.v1.api import api_router
from backend.core.config import settings
from backend.areas.finder import area_finder
from backend.pages.pages import pages_router


app = FastAPI()
app.mount('/static', StaticFiles(directory=settings.STATIC_DIR), name='static')
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(pages_router)


@app.on_event('startup')
def load_areas_data() -> None:
    area_finder.load_data()
