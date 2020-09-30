from databases import Database

from app.domain.models.user import User
from app.domain.services.user_service import UserService


class UserRdbService(UserService):
    def __init__(self, database: Database) -> None:
        self.__database = database

    async def duplicate_username(self, user: User) -> bool:
        query = "SELECT count(*) FROM users WHERE username = :username OR id != :id"
        values = {"username": user.username.value, "id": user.id.value}
        count: int = await self.__database.execute(query, values)
        return count > 0

    async def duplicate_email(self, user: User) -> bool:
        query = "SELECT count(*) FROM users WHERE email = :email OR id != :id"
        values = {"email": user.email.value, "id": user.id.value}
        count: int = await self.__database.execute(query, values)
        return count > 0
