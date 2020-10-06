import uuid

import pytest
from pytest_mock import MockerFixture

from app.application.commands.user_create_command import (
    UserCreateCommand,
    UserCreateCommandInteractor,
    UserCreateCommandRequest,
)
from app.application.shared.logger import Logger
from app.domain.models.email import Email
from app.domain.models.user import User
from app.domain.models.user_value_object import (
    UserDuplicatedError,
    UserFirstName,
    UserId,
    UserLastName,
    UserName,
)
from app.domain.repositories.unit_of_work import UnitOfWork
from app.domain.repositories.users_repository import UsersRepository
from app.domain.services.user_service import UserService


class TestUserCreateCommand(object):
    @pytest.mark.asyncio
    async def test_NG_execute_when_not_iplemented(self, mocker: MockerFixture) -> None:
        """[異常系]UserCreateCommandクラスのexecuteメソッドが未実装で例外が投げられる."""
        command = UserCreateCommand()
        mock_request = mocker.Mock(UserCreateCommandRequest)
        with pytest.raises(NotImplementedError):
            await command.execute(mock_request)


@pytest.fixture(scope="function")
def test_request() -> UserCreateCommandRequest:
    return UserCreateCommandRequest(
        username=UserName("testuser"),
        email=Email("test@test.com"),
        first_name=UserFirstName("ftest"),
        last_name=UserLastName("ltest"),
    )


class TestUserCreateCommandInteractor(object):
    @pytest.mark.asyncio
    async def test_OK_execute(
        self, mocker: MockerFixture, test_request: UserCreateCommandRequest
    ) -> None:
        """[正常系]ユーザを作成できる."""

        fixed_uuid = uuid.uuid4()
        mocker.patch.object(uuid, "uuid4", return_value=fixed_uuid)

        test_user = User(
            id=UserId(),
            username=test_request.username,
            email=test_request.email,
            first_name=test_request.first_name,
            last_name=test_request.last_name,
        )

        mock_users_repository = mocker.Mock(UsersRepository)
        mock_users_repository_add = mocker.patch.object(
            mock_users_repository, "add", return_value=test_user
        )

        unit_of_work = UnitOfWork(users_repository=mock_users_repository)
        unit_of_work_begin = mocker.patch.object(unit_of_work, "begin")
        unit_of_work_commit = mocker.patch.object(unit_of_work, "commit")

        mock_user_service = mocker.Mock(UserService)
        mock_user_service_verify_duplicate_user = mocker.spy(
            mock_user_service, "verify_duplicate_user"
        )

        mock_logger = mocker.Mock(Logger)
        mock_logger_info = mocker.spy(mock_logger, "info")

        interactor = UserCreateCommandInteractor(
            unit_of_work=unit_of_work,
            user_service=mock_user_service,
            logger=mock_logger,
        )

        response = await interactor.execute(test_request)

        assert mock_logger_info.call_count == 2

        assert unit_of_work_begin.call_count == 1
        assert unit_of_work_commit.call_count == 1

        assert mock_user_service_verify_duplicate_user.call_count == 1

        assert mock_users_repository_add.call_count == 1
        assert mock_users_repository_add.call_args.args[0].id == test_user.id

        assert response.id == test_user.id

    @pytest.mark.asyncio
    async def test_NG_execute_duplicate_error(
        self, mocker: MockerFixture, test_request: UserCreateCommandRequest
    ) -> None:
        """[異常系]ユーザ作成時に例外が発生し、ロールバックされる."""
        fixed_uuid = uuid.uuid4()
        mocker.patch.object(uuid, "uuid4", return_value=fixed_uuid)

        mock_users_repository = mocker.Mock(UsersRepository)

        unit_of_work = UnitOfWork(users_repository=mock_users_repository)
        unit_of_work_begin = mocker.patch.object(unit_of_work, "begin")
        unit_of_work_commit = mocker.patch.object(unit_of_work, "commit")
        unit_of_work_rollback = mocker.patch.object(unit_of_work, "rollback")

        mock_user_service = mocker.Mock(UserService)
        mock_user_service_verify_duplicate_user = mocker.patch.object(
            mock_user_service,
            "verify_duplicate_user",
            side_effect=UserDuplicatedError(["username"]),
        )

        mock_logger = mocker.Mock(Logger)
        mock_logger_info = mocker.spy(mock_logger, "info")
        mock_logger_error = mocker.spy(mock_logger, "error")

        interactor = UserCreateCommandInteractor(
            unit_of_work=unit_of_work,
            user_service=mock_user_service,
            logger=mock_logger,
        )

        with pytest.raises(Exception) as e:
            await interactor.execute(test_request)

        assert mock_logger_info.call_count == 1
        assert mock_logger_error.call_count == 1

        assert unit_of_work_begin.call_count == 1
        assert unit_of_work_commit.call_count == 0
        assert unit_of_work_rollback.call_count == 1

        assert mock_user_service_verify_duplicate_user.call_count == 1

        assert isinstance(e.value, UserDuplicatedError)
