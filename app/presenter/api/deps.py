from app.domain.repositories.users_repository import UsersRepository
from app.application.commands.user_create_command import (
    UserCreateCommand,
    UserCreateCommandInteractor,
)
from app.infrastructure.repositories.users_rdb_repository import UsersRdbRepository

from fastapi import Depends


def create_users_repository() -> UsersRepository:
    return UsersRdbRepository()


def create_user_create_command(
    users_repository: UsersRepository = Depends(create_users_repository),
) -> UserCreateCommand:
    return UserCreateCommandInteractor(users_repository)

