from fastapi import APIRouter, Depends

from app.application.commands.user_create_command import UserCreateCommand
from app.application.query_services.users_get_query_service import (
    UsersGetQueryService,
    UsersGetQueryServiceResponse,
)
from app.presenter.api.deps import (
    create_user_create_command,
    create_users_get_query_service,
)
from app.presenter.api.dto.user import (
    UserCreateCommandPresenter,
    UserCreateCommandRequestDto,
    UserCreateCommandResponseDto,
    UsersGetQueryServicePresenter,
    UsersGetQueryServiceRequestDto,
)

router = APIRouter()


@router.get(
    path="/",
    responses={
        200: {
            "model": UsersGetQueryServiceResponse,
            "title": "ユーザ取得",
            "description": "ユーザ取得レスポンス",
        }
    },
)
async def get_users(
    request: UsersGetQueryServiceRequestDto = Depends(UsersGetQueryServiceRequestDto),
    query_service: UsersGetQueryService = Depends(create_users_get_query_service),
) -> UsersGetQueryServiceResponse:
    presenter = UsersGetQueryServicePresenter()
    query_request = presenter.to_query_request(request)

    query_result = await query_service.execute(query_request)

    return query_result


@router.post(
    path="/",
    responses={
        200: {
            "model": UserCreateCommandResponseDto,
            "title": "ユーザ作成成功",
            "description": "ユーザ作成成功レスポンス",
        }
    },
)
async def create_user(
    request: UserCreateCommandRequestDto,
    command: UserCreateCommand = Depends(create_user_create_command),
) -> UserCreateCommandResponseDto:
    presenter = UserCreateCommandPresenter()

    command_request = presenter.to_command_request(request)

    command_result = await command.excecute(command_request)

    response = presenter.to_response_dto(command_result)

    return response
