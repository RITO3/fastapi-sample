from abc import ABCMeta, abstractclassmethod

from app.domain.models.user import User


class UsersRepository(object):
    __metaclass__ = ABCMeta

    @abstractclassmethod
    def add(self, user: User) -> User:
        raise NotImplementedError()
