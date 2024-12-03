from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.core.config import settings

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)
pages_router = APIRouter()


@pages_router.get('/status', response_class=HTMLResponse)
async def get_import_status(request: Request):
    return templates.TemplateResponse(request=request, name='status.html')
