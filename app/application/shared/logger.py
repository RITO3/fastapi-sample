from abc import ABCMeta, abstractmethod
from typing import Any


class Logger(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def info(self, msg: Any) -> None:
        raise NotImplementedError()

    @abstractmethod
    def error(self, msg: Any) -> None:
        raise NotImplementedError()
