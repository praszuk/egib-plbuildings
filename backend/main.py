from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pythonjsonlogger import jsonlogger
from starlette.requests import Request

from backend.api.v1.api import api_router
from backend.core.config import settings
from backend.core.logger import access_logger
from backend.areas.finder import area_finder
from backend.pages.pages import pages_router, generate_manifest


@asynccontextmanager
async def lifespan(_):
    area_finder.load_data()
    generate_manifest()
    yield


app = FastAPI(lifespan=lifespan)
app.mount('/static', StaticFiles(directory=settings.STATIC_DIR), name='static')
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(pages_router)


@app.middleware('http')
async def log_access(request: Request, call_next):
    client_addr = request.client.host if request.client else 'Unknown'
    if request.url.query:
        request_line = (
            f'{request.method} {request.url.path}'
            f'?{request.url.query} HTTP/{request.scope["http_version"]}'
        )
    else:
        request_line = f'{request.method} {request.url.path} HTTP/{request.scope["http_version"]}'

    user_agent = request.headers.get('user-agent', 'Unknown')

    response = await call_next(request)
    status_code = response.status_code

    access_logger.info(
        '',
        extra={
            'client_addr': client_addr,
            'request_line': request_line,
            'status_code': status_code,
            'user_agent': user_agent,
        },
    )
    return response


class AccessJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(AccessJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['client_addr'] = log_record.get('client_addr', 'Unknown')
        log_record['request_line'] = log_record.get('request_line', 'Unknown')
        log_record['status_code'] = log_record.get('status_code', 'Unknown')
        log_record['user_agent'] = log_record.get('user_agent', 'Unknown')
