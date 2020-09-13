from app.domain.models.user import User
from app.domain.models.email import Email
from app.domain.models.user_value_object import (
    UserId,
    UserName,
    UserFirstName,
    UserLastName,
)
from app.domain.repositories.unit_of_work import UnitOfWork
from app.domain.services.user_service import UserService

from app.application.shared.logger import Logger

import dataclasses
from abc import ABCMeta, abstractclassmethod


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
    async def excecute(
        self, request: UserCreateCommandRequest
    ) -> UserCreateCommandResponse:
        raise NotImplementedError()


class UserCreateCommandInteractor(UserCreateCommand):
    def __init__(
        self, unit_of_work: UnitOfWork, user_service: UserService, logger: Logger
    ) -> None:
        self.__unit_of_work = unit_of_work
        self.__user_service = user_service
        self.__logger = logger

    async def excecute(
        self, request: UserCreateCommandRequest
    ) -> UserCreateCommandResponse:
        unit_of_work = self.__unit_of_work
        users_repository = self.__unit_of_work.users_repository
        logger = self.__logger

        try:
            user_id = UserId()
            new_user = User(
                user_id,
                request.username,
                request.email,
                request.first_name,
                request.last_name,
            )

            logger.info("Start UserCreateCommand.")
            await unit_of_work.begin()

            await self.__user_service.verify_duplicated_user(new_user)

            user = await users_repository.add(new_user)

            await unit_of_work.commit()
            logger.info("End UserCreateCommand.")
            return UserCreateCommandResponse(
                user.id, user.username, user.email, user.first_name, user.last_name
            )
        except Exception as e:
            logger.error(f"Rollback UserCreateCommand. {e}")
            await unit_of_work.rollback()
            raise e
