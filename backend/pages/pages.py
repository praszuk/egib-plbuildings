from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.areas.config import all_areas
from backend.core.config import settings

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)
pages_router = APIRouter()


@pages_router.get('/status', response_class=HTMLResponse)
async def get_import_status(request: Request):
    area_teryt_name = {teryt: area_parser.name for teryt, area_parser in all_areas.items()}
    return templates.TemplateResponse(
        request=request, name='status.html', context={'AREA_TERYT_NAME': area_teryt_name}
    )
