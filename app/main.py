from fastapi import FastAPI

from app.presenter.api.api import api_router
from app.presenter.api.deps import get_database
from app.presenter.middleware.exception_handler import configure_error_handlers


def create_application() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router, prefix="/api/v1")
    configure_error_handlers(app)
    return app


async def on_startup() -> None:
    database = get_database()
    await database.connect()


async def on_shutdown() -> None:
    database = get_database()
    await database.disconnect()


app = create_application()


@app.on_event("startup")
async def startup():
    await on_startup()


@app.on_event("shutdown")
async def shutdown():
    await on_shutdown()
