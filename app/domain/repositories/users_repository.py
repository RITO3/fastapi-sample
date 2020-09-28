from abc import ABCMeta, abstractclassmethod

from app.domain.models.user import User
from app.domain.repositories.repository import Repository


class UsersRepository(Repository):
    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        super().__init__()

    @abstractclassmethod
    async def add(self, user: User) -> User:
        raise NotImplementedError()
