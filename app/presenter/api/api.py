from fastapi import APIRouter

from app.presenter.api.dto.erro_dto import BadRequestDto
from app.presenter.api.endpoints import users

api_router = APIRouter()

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    responses={400: {"model": BadRequestDto}, 422: {}},
)
