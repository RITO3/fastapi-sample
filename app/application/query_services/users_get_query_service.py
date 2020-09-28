"""[クエリ]ユーザ取得クエリ.

以下のクラスを有します.

    * UsersGetQueryRequest
    * UsersGetQueryResponse
    * UsersGetQueryService

"""

import dataclasses
from abc import ABCMeta, abstractmethod
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.models.page import Page


@dataclasses.dataclass(frozen=True)
class UsersGetQueryServiceRequest:
    """UsersGetQueryServiceRequestクラス."""

    page: Page


class UsersGetQueryServiceUser(BaseModel):
    """UsersGetQueryServiceUserクラス.

    UsersGetQueryServiceで使用するユーザクラスです.

    Attributes:
        id (UUID): ユーザID
        username (str): ユーザ名
    """

    id: UUID = Field(..., title="ユーザID", description="ユーザID")
    username: str = Field(..., title="ユーザ名", description="ユーザ名")


class UsersGetQueryServiceResponse(BaseModel):
    """UsersGetQueryResponseクラス.

    Attributes:
        users (List[UsersGetQueryUser]): ユーザ
        page (Page): ページ情報
    """

    users: List[UsersGetQueryServiceUser] = Field(
        ..., title="ユーザ一覧", description="ユーザ一覧"
    )


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
