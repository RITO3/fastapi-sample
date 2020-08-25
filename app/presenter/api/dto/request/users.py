from app.domain.models.user_value_object import (
    UserName,
    UserLastName,
    UserFirstName,
)
from app.domain.models.email import Email
from app.application.commands.user_create_command import UserCreateCommandRequest

from app.presenter.api.dto.shared.page_dto import PageQueryParameterDto
from pydantic import BaseModel, Field


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
    email: str = Field("", title="Email")
    first_name: str = Field("", title="名", min_length=3, max_length=16)
    last_name: str = Field("", title="姓", min_length=3, max_length=16)

    def create_command_request(self) -> UserCreateCommandRequest:
        return UserCreateCommandRequest(
            UserName(self.username),
            Email(self.email),
            UserFirstName(self.first_name),
            UserLastName(self.last_name),
        )
