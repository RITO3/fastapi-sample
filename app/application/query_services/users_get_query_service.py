"""[クエリ]ユーザ取得クエリ.

以下のクラスを有します.

    * UsersGetQueryRequest
    * UsersGetQueryResponse
    * UsersGetQueryService

"""

from abc import ABCMeta, abstractmethod
from typing import List
from uuid import UUID

from pydantic import BaseModel


class UsersGetQueryServiceRequest:
    """UsersGetQueryServiceRequestクラス."""

    pass


class UsersGetQueryServiceUser(BaseModel):
    """UsersGetQueryServiceUserクラス.

    UsersGetQueryServiceで使用するユーザクラスです.

    Attributes:
        id (UUID): ユーザID
        username (str): ユーザ名
    """

    id: UUID
    username: str


class UsersGetQueryServiceResponse(BaseModel):
    """UsersGetQueryResponseクラス.

    Attributes:
        users (List[UsersGetQueryUser]): ユーザ
        page (Page): ページ情報
    """

    users: List[UsersGetQueryServiceUser]


class UsersGetQueryService(object):
    """UsersGetQueryServiceクラス."""

    __metaclass__ = ABCMeta

    @abstractmethod
    async def execute(
        self, req: UsersGetQueryServiceRequest
    ) -> UsersGetQueryServiceResponse:
        """クエリ実行処理.

        Args:
            req (UsersGetQueryServiceRequest): リクエスト

        Raises:
            NotImplementedError: 継承したサブクラスが未実装だった場合に、例外を投げます.

        Returns:
            UsersGetQueryServiceResponse: レスポンス
        """
        raise NotImplementedError()
