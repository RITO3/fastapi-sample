from typing import List
from app.presenter.api.dto.erro_dto import BadRequestDto, BadRequestParameter
from app.domain.models.user_value_object import UserDuplicatedError

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


def user_duplicated_error_handler(request: Request, exc: UserDuplicatedError):
    parameters: List[BadRequestParameter] = list()

    for paramater in exc.parameters:
        parameters.append(
            BadRequestParameter(name=paramater, message=f"{paramater}が重複しています。")
        )

    error_dto = BadRequestDto(message=exc.message, parameters=parameters)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(error_dto)
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    parameters: List[BadRequestParameter] = list()
    for error in exc.errors():
        parameters.append(
            BadRequestParameter(name=error["loc"][1], message=error["msg"])
        )
    error_dto = BadRequestDto(message="入力値が不正です。", parameters=parameters)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(error_dto)
    )


def configure_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UserDuplicatedError, user_duplicated_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
