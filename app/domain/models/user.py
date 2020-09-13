"""ユーザクラス.

ユーザは以下の情報を持ちます.

* ユーザID
* ユーザ名

"""

from app.domain.models.email import Email
from app.domain.models.user_value_object import (
    UserFirstName,
    UserId,
    UserLastName,
    UserName,
)


class User:
    """ユーザクラス.
    Attributes:
        user_id (UserId): ユーザID
        username (UserName): ユーザ名
    """

    def __init__(
        self,
        user_id: UserId,
        user_name: UserName,
        email: Email,
        first_name: UserFirstName,
        last_name: UserLastName,
    ):
        """初期化処理.

        Args:
            user_id (UserId): ユーザID
            username (UserName): ユーザ名
        """
        self.__id = user_id
        self.__username = user_name
        self.__email = email
        self.__first_name = first_name
        self.__last_name = last_name

    @property
    def id(self) -> UserId:
        return self.__id

    @property
    def username(self) -> UserName:
        return self.__username

    @property
    def email(self) -> Email:
        return self.__email

    @property
    def first_name(self) -> UserFirstName:
        return self.__first_name

    @property
    def last_name(self) -> UserLastName:
        return self.__last_name

    def __str__(self) -> str:
        return "ID:{},Name:{},Email:{},First Name:{},Last Name:{}".format(
            self.__id,
            self.__username,
            self.__email,
            self.__first_name,
            self.__last_name,
        )
