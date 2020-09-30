import pytest

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
    async def test_OK_verify_duplicate_user(self, test_user: User) -> None:
        """[正常系]ユーザの重複チェックで例外が投げられない."""

        class UserServiceImpl(UserService):
            async def duplicate_username(self, user: User) -> bool:
                return False

            async def duplicate_email(self, user: User) -> bool:
                return False

        user_service = UserServiceImpl()
        await user_service.verify_duplicate_user(user=test_user)

    @pytest.mark.asyncio
    async def test_NG_verify_duplicate_user_when_duplicate_username(
        self, test_user: User
    ) -> None:
        """[異常系]ユーザの重複チェックで例外が投げられる(ユーザ名が重複)."""

        class UserServiceImpl(UserService):
            async def duplicate_username(self, user: User) -> bool:
                return True

            async def duplicate_email(self, user: User) -> bool:
                return False

        with pytest.raises(UserDuplicatedError):
            user_service = UserServiceImpl()
            await user_service.verify_duplicate_user(user=test_user)
