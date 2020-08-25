from app.domain.models.user import User
from app.domain.models.email import Email
from app.domain.models.user_value_object import (
    UserId,
    UserName,
    UserFirstName,
    UserLastName,
)

from app.domain.repositories.users_repository import UsersRepository


import dataclasses
from abc import ABCMeta, abstractclassmethod

# import inject


@dataclasses.dataclass(frozen=True)
class UserCreateCommandRequest:
    username: UserName
    email: Email
    first_name: UserFirstName
    last_name: UserLastName


@dataclasses.dataclass(frozen=True)
class UserCreateCommandResponse:
    id: UserId
    username: UserName
    email: Email
    first_name: UserFirstName
    last_name: UserLastName
    # audit_time: AuditTime


class UserCreateCommand(object):
    __metaclass__ = ABCMeta

    @abstractclassmethod
    def excecute(self, request: UserCreateCommandRequest) -> UserCreateCommandResponse:
        raise NotImplementedError()


class UserCreateCommandInteractor(UserCreateCommand):
    def __init__(self, users_repository: UsersRepository) -> None:
        self.__users_repository = users_repository

    def excecute(self, request: UserCreateCommandRequest) -> UserCreateCommandResponse:
        user_id = UserId()
        new_user = User(
            user_id,
            request.username,
            request.email,
            request.first_name,
            request.last_name,
        )
        user = self.__users_repository.add(new_user)

        return UserCreateCommandResponse(
            user.id, user.username, user.email, user.first_name, user.last_name
        )
