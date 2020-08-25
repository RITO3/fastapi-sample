from app.domain.models.user import User
from app.domain.repositories.users_repository import UsersRepository


class UsersRdbRepository(UsersRepository):
    def __init__(self) -> None:
        return

    def add(self, user: User) -> User:
        print(user)
        return user
