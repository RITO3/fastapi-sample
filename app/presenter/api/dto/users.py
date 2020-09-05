from app.application.query_services.users_get_query_service import (
    UsersGetQueryServiceRequest,
)
from app.domain.models.user_value_object import (
    UserName,
    UserLastName,
    UserFirstName,
)
from app.domain.models.email import Email
from app.application.commands.user_create_command import (
    UserCreateCommandRequest,
    UserCreateCommandResponse,
)

from app.presenter.api.dto.page_dto import PageQueryParameterDto
from pydantic import BaseModel, Field, EmailStr
import uuid


class UsersGetQueryServiceRequestDto(PageQueryParameterDto):
    """UsersGetQueryServiceDtoクラス."""


class UserCreateCommandRequestDto(BaseModel):
    """UserCreateCommandRequestDtoクラス.

    Attributes:
        username (str): ユーザ名
        email (str): Eメール
        first_name (str): 名
        last_name (str): 姓
    """

    username: str = Field("", title="ユーザ名", min_length=3, max_length=16)
    email: EmailStr = Field("", title="Email")
    first_name: str = Field("", title="名", min_length=3, max_length=16)
    last_name: str = Field("", title="姓", min_length=3, max_length=16)


class UserCreateCommandResponseDto(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str


class UsersGetQueryServicePresenter:
    def to_query_request(
        self, request: UsersGetQueryServiceRequestDto
    ) -> UsersGetQueryServiceRequest:
        return UsersGetQueryServiceRequest()


class UserCreateCommandPresenter:
    def to_command_request(
        self, request: UserCreateCommandRequestDto,
    ) -> UserCreateCommandRequest:
        return UserCreateCommandRequest(
            username=UserName(request.username),
            email=Email(request.email),
            first_name=UserFirstName(request.first_name),
            last_name=UserLastName(request.last_name),
        )

    def to_response_dto(
        self, command_response: UserCreateCommandResponse,
    ) -> UserCreateCommandResponseDto:
        return UserCreateCommandResponseDto(
            id=command_response.id.value,
            username=command_response.username.value,
            email=command_response.email.value,
            first_name=command_response.first_name.value,
            last_name=command_response.last_name.value,
        )
