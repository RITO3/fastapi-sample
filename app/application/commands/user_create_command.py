import dataclasses
from abc import ABCMeta, abstractclassmethod

from app.application.shared.logger import Logger
from app.domain.models.email import Email
from app.domain.models.user import User
from app.domain.models.user_value_object import (
    UserFirstName,
    UserId,
    UserLastName,
    UserName,
)
from app.domain.repositories.unit_of_work import UnitOfWork
from app.domain.services.user_service import UserService


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


class UserCreateCommand(object):
    __metaclass__ = ABCMeta

    @abstractclassmethod
    async def execute(
        self, request: UserCreateCommandRequest
    ) -> UserCreateCommandResponse:
        raise NotImplementedError()


@dataclasses.dataclass(frozen=True)
class UserCreateCommandInteractor(UserCreateCommand):

    unit_of_work: UnitOfWork
    user_service: UserService
    logger: Logger

    async def execute(
        self, request: UserCreateCommandRequest
    ) -> UserCreateCommandResponse:

        try:
            user_id = UserId()
            new_user = User(
                id=user_id,
                username=request.username,
                email=request.email,
                first_name=request.first_name,
                last_name=request.last_name,
            )

            self.logger.info("Start UserCreateCommand.")
            await self.unit_of_work.begin()

            await self.user_service.verify_duplicate_user(new_user)
            created_user = await self.unit_of_work.users_repository.add(new_user)

            await self.unit_of_work.commit()
            self.logger.info("End UserCreateCommand.")
            return UserCreateCommandResponse(
                id=created_user.id,
                username=created_user.username,
                email=created_user.email,
                first_name=created_user.first_name,
                last_name=created_user.last_name,
            )
        except Exception as e:
            self.logger.error(f"Rollback UserCreateCommand. {e}")
            await self.unit_of_work.rollback()
            raise e
