import pytest
from pytest_mock import MockerFixture

from app.application.query_services.users_get_query_service import (
    UsersGetQueryService,
    UsersGetQueryServiceRequest,
)


class TestUsersGetQueryService(object):
    @pytest.mark.asyncio
    async def test_NG_execute_when_not_iplemented(self, mocker: MockerFixture) -> None:
        """[異常系] UsersGetQueryServiceクラスのexecuteメソッドが未実装で例外が投げられる."""
        query_service = UsersGetQueryService()
        mock_request = mocker.Mock(UsersGetQueryServiceRequest)
        with pytest.raises(NotImplementedError):
            await query_service.execute(mock_request)
