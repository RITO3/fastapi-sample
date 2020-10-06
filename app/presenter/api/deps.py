from databases import Database
from fastapi import Depends

from app.application.commands.user_create_command import (
    UserCreateCommand,
    UserCreateCommandInteractor,
)
from app.application.query_services.users_get_query_service import UsersGetQueryService
from app.application.shared.logger import Logger
from app.domain.repositories.unit_of_work import UnitOfWork
from app.domain.repositories.users_repository import UsersRepository
from app.domain.services.user_service import UserService
from app.infrastructure.logger.unicorn_logger import UnicornLogger
from app.infrastructure.query_services.users_get_rdb_query_service import (
    UsersGetRdbQueryService,
)
from app.infrastructure.repositories.rdb_uint_of_work import RdbUnitOfWork
from app.infrastructure.repositories.users_rdb_repository import UsersRdbRepository
from app.infrastructure.services.user_rdb_service import UserRdbService
from app.presenter.api.db import database


def get_logger() -> Logger:
    return UnicornLogger()


def get_database() -> Database:
    return database


def create_users_repository(
    database: Database = Depends(get_database),
) -> UsersRepository:
    return UsersRdbRepository(database)


def create_user_service(database: Database = Depends(get_database),) -> UserService:
    return UserRdbService(database)


def create_unit_of_work(
    database: Database = Depends(get_database),
    users_repositry: UsersRepository = Depends(create_users_repository),
) -> UnitOfWork:
    return RdbUnitOfWork(database, users_repositry)


def create_users_get_query_service(
    database: Database = Depends(get_database),
) -> UsersGetQueryService:
    return UsersGetRdbQueryService(database)


def create_user_create_command(
    unit_of_work: UnitOfWork = Depends(create_unit_of_work),
    user_service: UserService = Depends(create_user_service),
    logger: Logger = Depends(get_logger),
) -> UserCreateCommand:
    return UserCreateCommandInteractor(unit_of_work, user_service, logger)
