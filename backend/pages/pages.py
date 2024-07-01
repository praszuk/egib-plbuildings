from datetime import datetime
import json

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.core.config import settings
from backend.areas.models import HealthCheckReport

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)
pages_router = APIRouter()


def format_dt(utc_dt: str, dt_format: str) -> str:
    return datetime.fromisoformat(utc_dt).strftime(dt_format)


templates.env.filters['format_dt'] = format_dt


@pages_router.get('/status', response_class=HTMLResponse)
async def get_areas_healthcheck_status(request: Request):
    try:
        with open(settings.AREAS_HEALTHCHECK_CACHE_FILENAME, 'r') as f:
            healthcheck_report = json.load(f)

    except IOError:
        healthcheck_report = HealthCheckReport('', '', {}, {})

    return templates.TemplateResponse(
        request=request, name='status.html', context={'healthcheck_report': healthcheck_report}
    )
