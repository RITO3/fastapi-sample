from abc import ABCMeta, abstractmethod

from app.domain.repositories.users_repository import UsersRepository


class UnitOfWork(object):
    __metaclass__ = ABCMeta

    def __init__(self, users_repository: UsersRepository) -> None:
        self.__users_repository = users_repository

    @property
    def users_repository(self) -> UsersRepository:
        return self.__users_repository

    @abstractmethod
    async def begin(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError()
