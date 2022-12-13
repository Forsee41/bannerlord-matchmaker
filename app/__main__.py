import logging

from .config import setup_loggers


setup_loggers()
log = logging.getLogger(__name__)

