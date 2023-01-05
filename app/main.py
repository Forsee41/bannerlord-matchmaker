import uvicorn

from app.api.app_builder import create_app
from app.log_config import setup_loggers

__VERSION__ = "0.1.0"
setup_loggers()
app = create_app()


def main() -> None:
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
