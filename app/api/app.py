from fastapi import FastAPI
import logging

from . import routes


log = logging.getLogger(__name__)


def register_routers(app: FastAPI) -> None:
    app.include_router(routes.players_router)
    app.include_router(routes.config_router)


def register_events(app: FastAPI) -> None:
    @app.on_event("startup")
    async def init_app():
        log.info("Starting FastAPI app server")

    assert init_app


def create_app() -> FastAPI:
    app = FastAPI()
    register_events(app)
    register_routers(app)

    return app


app = create_app()
