from app.application.query_services.users_get_query_service import (
    UsersGetQueryService,
    UsersGetQueryServiceResponse,
)
from app.application.commands.user_create_command import UserCreateCommand
from app.presenter.api.dto.users import (
    UserCreateCommandPresenter,
    UserCreateCommandRequestDto,
    UserCreateCommandResponseDto,
    UsersGetQueryServicePresenter,
    UsersGetQueryServiceRequestDto,
)

from app.presenter.api.deps import (
    create_user_create_command,
    create_users_get_query_service,
)
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/", response_model=UsersGetQueryServiceResponse)
async def get_users(
    request: UsersGetQueryServiceRequestDto = Depends(UsersGetQueryServiceRequestDto),
    query_service: UsersGetQueryService = Depends(create_users_get_query_service),
) -> UsersGetQueryServiceResponse:
    presenter = UsersGetQueryServicePresenter()
    query_request = presenter.to_query_request(request)

    query_result = await query_service.execute(query_request)

    return query_result


@router.post("/", response_model=UserCreateCommandResponseDto)
async def create_user(
    request: UserCreateCommandRequestDto,
    command: UserCreateCommand = Depends(create_user_create_command),
) -> UserCreateCommandResponseDto:
    presenter = UserCreateCommandPresenter()

    command_request = presenter.to_command_request(request)

    command_result = await command.excecute(command_request)

    response = presenter.to_response_dto(command_result)

    return response
