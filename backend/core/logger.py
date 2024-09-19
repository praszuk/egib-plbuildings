from logging import getLogger

from backend.core.config import settings

access_logger = getLogger(settings.ACCESS_LOGGER)
default_logger = getLogger(settings.DEFAULT_LOGGER)
