import logging

from .api.app import create_app
from .config import setup_loggers


__VERSION__ = "0.1.0"


setup_loggers()
log = logging.getLogger(__name__)

app = create_app()
