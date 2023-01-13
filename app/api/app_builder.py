import logging

from fastapi import FastAPI

from app.config import main_service_config

from . import routes

log = logging.getLogger(__name__)


def register_routers(app: FastAPI) -> None:
    app.include_router(routes.players_router)
    app.include_router(routes.config_router)
    app.include_router(routes.test_router)


def register_events(app: FastAPI) -> None:
    @app.on_event("startup")
    async def init_app():
        log.info("Starting FastAPI app server")
        log.info(
            "Token refresh time is "
            f"{main_service_config.token_refresh_time_seconds} seconds"
        )

    assert init_app


def create_app() -> FastAPI:
    app = FastAPI()
    register_events(app)
    register_routers(app)

    return app
