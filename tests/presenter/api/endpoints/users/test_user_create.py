import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from app.application.commands.user_create_command import (
    UserCreateCommand,
    UserCreateCommandResponse,
)
from app.domain.models.email import Email
from app.domain.models.user_value_object import (
    UserDuplicatedError,
    UserFirstName,
    UserId,
    UserLastName,
    UserName,
)
from app.main import create_application
from app.presentation.api.deps import create_user_create_command


@pytest.fixture(scope="function")
async def test_OK_create_user_client(mocker: MockerFixture):
    app = create_application()
    app.dependency_overrides.clear()

    def create_mock_create_user_command():
        test_response = UserCreateCommandResponse(
            id=UserId(),
            username=UserName("testuser"),
            email=Email("test@test.com"),
            first_name=UserFirstName("fuser"),
            last_name=UserLastName("luser"),
        )
        mock_user_create_command = mocker.Mock(UserCreateCommand)
        mocker.patch.object(
            mock_user_create_command, "execute", return_value=test_response
        )
        return mock_user_create_command

    app.dependency_overrides.setdefault(
        create_user_create_command, create_mock_create_user_command
    )

    async with AsyncClient(
        app=app, base_url="http://localhost", headers={"Accept-Language": "ja"}
    ) as client:
        yield client


@pytest.fixture(scope="function")
async def test_NG_create_user_client_with_duplicate_user(mocker: MockerFixture):
    app = create_application()
    app.dependency_overrides.clear()

    def create_mock_create_user_command():
        mock_user_create_command = mocker.Mock(UserCreateCommand)
        mocker.patch.object(
            mock_user_create_command,
            "execute",
            side_effect=UserDuplicatedError(["username", "email"]),
        )
        return mock_user_create_command

    app.dependency_overrides.setdefault(
        create_user_create_command, create_mock_create_user_command
    )

    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client


class TestUserCreate(object):
    @pytest.mark.asyncio
    async def test_OK_create_user(
        self, test_OK_create_user_client: AsyncClient
    ) -> None:
        """[正常系]ユーザを作成できる."""
        post_data = {
            "username": "testuser",
            "email": "test@test.com",
            "first_name": "fuser",
            "last_name": "luser",
        }

        response = await test_OK_create_user_client.post(
            "/api/v1/users", json=post_data,
        )

        assert response.status_code == 201

        json_object = response.json()
        assert json_object["username"] == post_data["username"]
        assert json_object["email"] == post_data["email"]
        assert json_object["first_name"] == post_data["first_name"]
        assert json_object["last_name"] == post_data["last_name"]

    @pytest.mark.asyncio
    async def test_NG_create_user_when_invalid_request(
        self, test_OK_create_user_client: AsyncClient
    ) -> None:
        """[異常系]ユーザを作成できない(パラメータ不備)."""
        post_data = {
            "username": "te",
            "email": "invalid_email",
            "first_name": "fu",
            "last_name": "lu",
        }

        response = await test_OK_create_user_client.post(
            "/api/v1/users", json=post_data,
        )

        assert response.status_code == 400
        assert response.json() == {
            "message": "不正な入力値です",
            "parameters": [
                {"name": "username", "message": "入力値が3文字以上か確認してください",},
                {"name": "email", "message": "入力値がEmailの形式ではないです"},
                {"name": "first_name", "message": "入力値が3文字以上か確認してください",},
                {"name": "last_name", "message": "入力値が3文字以上か確認してください",},
            ],
        }

    @pytest.mark.asyncio
    async def test_NG_create_user_when_duplicate_user(
        self, test_NG_create_user_client_with_duplicate_user: AsyncClient
    ) -> None:
        """[異常系]ユーザを作成できない(パラメータ不備)."""
        post_data = {
            "username": "testuser",
            "email": "test@test.com",
            "first_name": "fuser",
            "last_name": "luser",
        }

        response = await test_NG_create_user_client_with_duplicate_user.post(
            "/api/v1/users", json=post_data,
        )

        assert response.status_code == 400
        assert response.json() == {
            "message": "ユーザが重複しています",
            "parameters": [
                {"name": "username", "message": "usernameが重複しています",},
                {"name": "email", "message": "emailが重複しています"},
            ],
        }
