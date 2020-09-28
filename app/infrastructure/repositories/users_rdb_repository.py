from databases.core import Database

from app.domain.models.user import User
from app.domain.repositories.users_repository import UsersRepository
from app.infrastructure.persistence.user import users


class UsersRdbRepository(UsersRepository):
    def __init__(self, database: Database) -> None:
        super().__init__()
        self.__database = database

    async def add(self, user: User) -> User:
        query = users.insert().values(
            id=user.id.value,
            username=user.username.value,
            email=user.email.value,
            first_name=user.first_name.value,
            last_name=user.last_name.value,
        )
        await self.__database.execute(query=query)
        return user
