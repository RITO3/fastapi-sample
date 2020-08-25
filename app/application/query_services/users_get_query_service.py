"""[クエリ]ユーザ取得クエリ.

以下のクラスを有します.

    * UsersGetQueryRequest
    * UsersGetQueryResponse
    * UsersGetQueryService

"""

import dataclasses
from abc import ABCMeta, abstractmethod
from typing import List

from app.domain.models.page import Page
from app.domain.models.user_value_object import UserId, UserName


class UsersGetQueryServiceRequest:
    """UsersGetQueryServiceRequestクラス."""


@dataclasses.dataclass(frozen=True)
class UsersGetQueryServiceUser:
    """UsersGetQueryServiceUserクラス.

    UsersGetQueryServiceで使用するユーザクラスです.

    Attributes:
        id (UserId): ユーザID
        username (UserName): ユーザ名
    """

    id: UserId
    username: UserName


@dataclasses.dataclass(frozen=True)
class UsersGetQueryServiceResponse:
    """UsersGetQueryResponseクラス.

    Attributes:
        users (List[UsersGetQueryUser]): ユーザ
        page (Page): ページ情報
    """

    users: List[UsersGetQueryServiceUser]
    page: Page


class UsersGetQueryService(object):
    """UsersGetQueryServiceクラス."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, req: UsersGetQueryServiceRequest) -> UsersGetQueryServiceResponse:
        """クエリ実行処理.

        Args:
            req (UsersGetQueryServiceRequest): リクエスト

        Raises:
            NotImplementedError: 継承したサブクラスが未実装だった場合に、例外を投げます.

        Returns:
            UsersGetQueryServiceResponse: レスポンス
        """
        raise NotImplementedError()
