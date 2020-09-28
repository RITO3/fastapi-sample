"""ユーザの値オブジェクトクラス群.

以下のクラスを有します.

    * UserIdクラス
    * UserNameクラス
    * UserLastNameクラス
    * UserFirstNameクラス
"""

import dataclasses
import uuid
from typing import List

from app.domain.shared.error import DomainError


class UserId:
    """UserIdクラス.

    ユーザIDは以下の形式です.

        * 形式: UUID
        * フォーマット: 不明

    Attributes:
        value (UUID): 値
    """

    def __init__(self, value: uuid.UUID = None) -> None:
        self.__value: uuid.UUID = value if value is not None else uuid.uuid4()

    @property
    def value(self) -> uuid.UUID:
        return self.__value

    def __str__(self) -> str:
        return str(self.__value)

    def __eq__(self, other: object) -> bool:
        """値が同じかどうか比較します.

        Args:
            other (object): 比較対象

        Returns:
            [bool]: 同じ値かどうか
        """
        return isinstance(other, UserId) and self.value == other.value


@dataclasses.dataclass(frozen=True)
class UserName:
    """UserNameクラス.

    Attributes:
        value (str): 値
    """

    value: str

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        """値が同じかどうか比較します.

        Args:
            other (object): 比較対象

        Returns:
            [bool]: 同じ値かどうか
        """
        return isinstance(other, UserName) and (self.value == other.value)


@dataclasses.dataclass(frozen=True)
class UserFirstName:
    value: str

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        """値が同じかどうか比較します.

        Args:
            other (object): 比較対象

        Returns:
            [bool]: 同じ値かどうか
        """
        return isinstance(other, UserFirstName) and (self.value == other.value)


@dataclasses.dataclass(frozen=True)
class UserLastName:
    value: str

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        """値が同じかどうか比較します.

        Args:
            other (object): 比較対象

        Returns:
            [bool]: 同じ値かどうか
        """
        return isinstance(other, UserLastName) and (self.value == other.value)


class UserDuplicatedError(DomainError):
    def __init__(self, parameters: List[str]):
        super().__init__("ユーザが重複しています。")
        self.parameters = parameters
