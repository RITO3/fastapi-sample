from app.application.shared.logger import Logger

from typing import Any
import logging


class UnicornLogger(Logger):
    def __init__(self) -> None:
        self.__logger = logging.getLogger("uvicorn")

    def info(self, mgs: Any) -> None:
        self.__logger.info(mgs)

    def error(self, msg: Any) -> None:
        self.__logger.error(msg)
