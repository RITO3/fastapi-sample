from fastapi import FastAPI

from app.presenter.api.api import api_router
from app.presenter.api.deps import get_database
from app.presenter.middleware.exception_handler import configure_error_handlers

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup():
    database = get_database()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    database = get_database()
    await database.disconnect()


configure_error_handlers(app)
