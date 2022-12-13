import logging

from .config import setup_loggers


__VERSION__ = "0.1.0"


setup_loggers()
log = logging.getLogger(__name__)

