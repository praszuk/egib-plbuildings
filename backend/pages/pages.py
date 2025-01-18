import hashlib
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.core.config import settings

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)
pages_router = APIRouter()

static_manifest = {}  # path: version (hash)


@pages_router.get('/status', response_class=HTMLResponse)
async def get_import_status(request: Request):
    return templates.TemplateResponse(request=request, name='status.html')


def generate_manifest():
    absolute_static_dir = Path(settings.STATIC_DIR)
    for file_path in absolute_static_dir.rglob('*.*'):
        relative_path_name = str(file_path.relative_to(absolute_static_dir))

        if relative_path_name.startswith('.') or relative_path_name.startswith('__'):
            continue

        with file_path.open('rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()[:8]
            static_manifest[relative_path_name] = file_hash


# Custom filter for static file versioning
def static_version(path: str) -> str:
    return f'/static/{path}?v={static_manifest.get(path)}'


templates.env.filters['static_version'] = static_version
