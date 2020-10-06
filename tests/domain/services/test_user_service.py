import pytest
from pytest_mock import MockerFixture

from app.domain.models.email import Email
from app.domain.models.user import User
from app.domain.models.user_value_object import (
    UserDuplicatedError,
    UserFirstName,
    UserId,
    UserLastName,
    UserName,
)
from app.domain.services.user_service import UserService


@pytest.fixture(scope="function")
def test_user() -> User:
    return User(
        id=UserId(),
        username=UserName("testuser"),
        email=Email("test@test.com"),
        first_name=UserFirstName("ftest"),
        last_name=UserLastName("ltest"),
    )


class TestUserService(object):
    @pytest.mark.asyncio
    async def test_OK_verify_duplicate_user(
        self, mocker: MockerFixture, test_user: User
    ) -> None:
        """[正常系]重複したユーザが存在しない."""

        user_service = UserService()
        user_service_duplicate_username = mocker.patch.object(
            user_service, "duplicate_username", return_value=False
        )
        user_service_duplicate_email = mocker.patch.object(
            user_service, "duplicate_email", return_value=False
        )

        await user_service.verify_duplicate_user(user=test_user)
        assert user_service_duplicate_username.call_count == 1
        assert user_service_duplicate_email.call_count == 1

    @pytest.mark.asyncio
    async def test_NG_verify_duplicate_user_when_duplicate_username(
        self, mocker: MockerFixture, test_user: User
    ) -> None:
        """[異常系]ユーザの重複チェックで例外が投げられる(ユーザ名が重複)."""

        user_service = UserService()
        user_service_duplicate_username = mocker.patch.object(
            user_service, "duplicate_username", return_value=True
        )
        user_service_duplicate_email = mocker.patch.object(
            user_service, "duplicate_email", return_value=False
        )

        with pytest.raises(UserDuplicatedError) as e:
            await user_service.verify_duplicate_user(user=test_user)

        assert user_service_duplicate_username.call_count == 1
        assert user_service_duplicate_email.call_count == 1
        assert e.value.parameters == ["username"]

    @pytest.mark.asyncio
    async def test_NG_verify_duplicate_user_when_duplicate_email(
        self, mocker: MockerFixture, test_user: User
    ) -> None:
        """[異常系]ユーザの重複チェックで例外が投げられる(Emailが重複)."""

        user_service = UserService()
        user_service_duplicate_username = mocker.patch.object(
            user_service, "duplicate_username", return_value=False
        )
        user_service_duplicate_email = mocker.patch.object(
            user_service, "duplicate_email", return_value=True
        )

        with pytest.raises(UserDuplicatedError) as e:
            await user_service.verify_duplicate_user(user=test_user)

        assert user_service_duplicate_username.call_count == 1
        assert user_service_duplicate_email.call_count == 1
        assert e.value.parameters == ["email"]
