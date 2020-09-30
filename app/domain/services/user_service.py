from abc import ABCMeta, abstractmethod
from typing import List

from app.domain.models.user import User
from app.domain.models.user_value_object import UserDuplicatedError


class UserService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def duplicate_username(self, user: User) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def duplicate_email(self, user: User) -> bool:
        raise NotImplementedError()

    async def verify_duplicate_user(self, user: User) -> None:
        paramater_names: List[str] = list()

        is_duplicated_username = await self.duplicate_username(user)

        if is_duplicated_username:
            paramater_names.append("username")

        is_duplicated_email = await self.duplicate_email(user)

        if is_duplicated_email:
            paramater_names.append("email")

        if len(paramater_names) > 0:
            raise UserDuplicatedError(paramater_names)
