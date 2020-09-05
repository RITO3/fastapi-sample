from app.domain.repositories.users_repository import UsersRepository
from app.domain.repositories.unit_of_work import UnitOfWork

from typing import Union
from databases import Database
from databases.core import Transaction

from asyncpg.exceptions import UniqueViolationError


class RdbUnitOfWork(UnitOfWork):
    __transaction: Union[Transaction, None] = None

    def __init__(self, database: Database, users_repository: UsersRepository) -> None:
        super().__init__(users_repository)
        self.__database = database

    @property
    def database(self) -> Database:
        return self.__database

    async def begin(self) -> None:
        self.__transaction = await self.__database.transaction()

    async def commit(self) -> None:
        if self.__transaction is None:
            raise Exception("transaction is not starting.")
        try:
            await self.__transaction.commit()
        except UniqueViolationError as uve:
            print("UniqueViolationError!!!!")
            print(uve)

            raise Exception(uve.as_dict())
        except Exception as e:
            raise e

    async def rollback(self) -> None:
        if self.__transaction is None:
            raise Exception("transaction is not starting.")
        await self.__transaction.rollback()
