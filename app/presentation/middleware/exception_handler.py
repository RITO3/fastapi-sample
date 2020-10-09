import dataclasses
from typing import List

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.domain.models.user_value_object import UserDuplicatedError
from app.presentation.api.dto.erro_dto import BadRequestDto, BadRequestParameter
from app.utils.i18n import i18n


@dataclasses.dataclass(frozen=True)
class AcceptLanguage:
    locale: str
    q: float


def sort_accept_language(accept_language: str) -> List[AcceptLanguage]:
    languages = accept_language.split(",")
    locale_q_pairs: List[AcceptLanguage] = list()
    for language in languages:
        if language.split(";")[0] == language:
            locale_q_pairs.append(AcceptLanguage(locale=language.strip(), q=1))
        else:
            locale = language.split(";")[0].strip()
            q = float(language.split(";")[1].split("=")[1])
            locale_q_pairs.append(AcceptLanguage(locale=locale, q=q))
    return sorted(locale_q_pairs, key=lambda x: (x.q), reverse=True)


def get_locale(request: Request) -> str:
    accept_language = request.headers.get("Accept-Language", "ja")
    sorted_accept_language = sort_accept_language(accept_language)
    return sorted_accept_language[0].locale.split("-")[0]


def user_duplicated_error_handler(request: Request, exc: UserDuplicatedError):
    locale = get_locale(request)
    parameters: List[BadRequestParameter] = list()

    for paramater in exc.parameters:
        message = i18n.t(
            "custom.duplicate.parameter", locale, **{"paramater": paramater}
        )
        parameters.append(BadRequestParameter(name=paramater, message=message))

    error_dto = BadRequestDto(
        message=i18n.t("custom.duplicate.user", locale), parameters=parameters
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(error_dto)
    )


def validation_exception_handler(request: Request, exc: RequestValidationError):
    locale = get_locale(request)
    parameters: List[BadRequestParameter] = list()
    for error in exc.errors():
        message = i18n.t(
            error["type"], locale, **error["ctx"] if "ctx" in error else dict()
        )
        parameters.append(BadRequestParameter(name=error["loc"][1], message=message))
    error_dto = BadRequestDto(
        message=i18n.t("custom.http.400_bad_request", locale), parameters=parameters
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(error_dto)
    )


def configure_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UserDuplicatedError, user_duplicated_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
