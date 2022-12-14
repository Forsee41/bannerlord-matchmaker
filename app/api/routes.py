import logging

from fastapi import APIRouter


log = logging.getLogger(__name__)

config_router = APIRouter(prefix="/config")
players_router = APIRouter(prefix="/players")
