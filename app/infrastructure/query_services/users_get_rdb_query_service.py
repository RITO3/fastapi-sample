from app.application.query_services.users_get_query_service import (
    UsersGetQueryService,
    UsersGetQueryServiceRequest,
    UsersGetQueryServiceResponse,
    UsersGetQueryServiceUser,
)

from databases import Database
from typing import List


class UsersGetRdbQueryService(UsersGetQueryService):
    def __init__(self, database: Database) -> None:
        self.__database = database

    async def execute(
        self, req: UsersGetQueryServiceRequest
    ) -> UsersGetQueryServiceResponse:

        users: List[UsersGetQueryServiceUser] = []
        query = "SELECT id,username FROM users LIMIT :limit OFFSET :offset"
        values = {"limit": req.page.page_size.value, "offset": req.page.offset}

        rows = await self.__database.fetch_all(query=query, values=values)

        for row in rows:
            users.append(
                UsersGetQueryServiceUser(id=row["id"], username=row["username"])
            )

        return UsersGetQueryServiceResponse(users=users)
