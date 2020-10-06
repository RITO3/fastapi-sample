import uuid
from typing import List

import pytest
from httpx import AsyncClient
from pytest_mock.plugin import MockerFixture

from app.application.query_services.users_get_query_service import (
    UsersGetQueryService,
    UsersGetQueryServiceResponse,
    UsersGetQueryServiceUser,
)
from app.main import create_application
from app.presenter.api.deps import create_users_get_query_service


@pytest.fixture(scope="function")
async def test_OK_get_users_client(mocker: MockerFixture):
    app = create_application()
    app.dependency_overrides.clear()

    def mock_users_get_query_service():
        users: List[UsersGetQueryServiceUser] = list()
        users.append(UsersGetQueryServiceUser(id=uuid.uuid4(), username="testuser1"))
        users.append(UsersGetQueryServiceUser(id=uuid.uuid4(), username="testuser2"))
        test_response = UsersGetQueryServiceResponse(users=users)
        mock_users_get_query_service = mocker.Mock(UsersGetQueryService)
        mocker.patch.object(
            mock_users_get_query_service, "execute", return_value=test_response
        )
        return mock_users_get_query_service

    app.dependency_overrides.setdefault(
        create_users_get_query_service, mock_users_get_query_service
    )

    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client


class TestUsersGet(object):
    @pytest.mark.asyncio
    async def test_OK_get_users(self, test_OK_get_users_client: AsyncClient) -> None:
        """[正常系]ユーザを取得することができる."""
        response = await test_OK_get_users_client.get("/api/v1/users")
        assert response.status_code == 200
        json_obj = response.json()
        assert json_obj["users"][0]["username"] == "testuser1"
        assert json_obj["users"][1]["username"] == "testuser2"

    @pytest.mark.asyncio
    async def test_OK_get_users_with_pagination(
        self, test_OK_get_users_client: AsyncClient
    ) -> None:
        """[正常系]ユーザを取得することができる(ページネーションあり)."""
        response = await test_OK_get_users_client.get(
            "/api/v1/users?page_size=100&page_number=1"
        )

        json_obj = response.json()

        assert response.status_code == 200
        assert json_obj["users"][0]["username"] == "testuser1"
        assert json_obj["users"][1]["username"] == "testuser2"

    @pytest.mark.asyncio
    async def test_NG_get_users_with_invalid_pagination_alphabet(
        self, test_OK_get_users_client: AsyncClient
    ) -> None:
        """[異常系]ユーザを取得することができない(ページネーションパラメータ誤り アルファベット)."""
        response = await test_OK_get_users_client.get(
            "/api/v1/users?page_size=a&page_number=a"
        )
        json_obj = response.json()
        assert response.status_code == 400
        assert json_obj == {
            "message": "入力値が不正です。",
            "parameters": [
                {"message": "value is not a valid integer", "name": "page_size"},
                {"message": "value is not a valid integer", "name": "page_number"},
            ],
        }

    @pytest.mark.asyncio
    async def test_NG_get_users_with_invalid_pagination_number(
        self, test_OK_get_users_client: AsyncClient
    ) -> None:
        """[異常系]ユーザを取得することができない(ページネーションパラメータ誤り 数値)."""
        response = await test_OK_get_users_client.get(
            "/api/v1/users?page_size=9&page_number=0"
        )
        json_obj = response.json()
        assert response.status_code == 400
        assert json_obj == {
            "message": "入力値が不正です。",
            "parameters": [
                {
                    "message": "ensure this value is greater than or equal to 10",
                    "name": "page_size",
                },
                {
                    "message": "ensure this value is greater than or equal to 1",
                    "name": "page_number",
                },
            ],
        }
