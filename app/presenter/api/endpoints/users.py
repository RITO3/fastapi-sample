from app.application.commands.user_create_command import UserCreateCommand
from app.presenter.api.dto.request.users import (
    UserCreateCommandRequestDto,
    UsersGetQueryServiceRequestDto,
)

from app.presenter.api.deps import create_user_create_command
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/")
def get_users(
    request: UsersGetQueryServiceRequestDto = Depends(UsersGetQueryServiceRequestDto),
):
    return request


@router.post("/")
def create_user(
    request: UserCreateCommandRequestDto,
    command: UserCreateCommand = Depends(create_user_create_command),
):
    command_request = request.create_command_request()
    command.excecute(command_request)
    return request
