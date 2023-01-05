import logging

from fastapi import APIRouter

log = logging.getLogger(__name__)

config_router = APIRouter(prefix="/config")
players_router = APIRouter(prefix="/players")
test_router = APIRouter(prefix="/test")


@test_router.post("/ping")
def test_routers():
    return {"test": True}
