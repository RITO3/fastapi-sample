from pydantic import BaseModel
from typing import Optional
from fastapi import Query


class PageQueryParameterDto:
    def __init__(
        self,
        page_size: Optional[int] = Query(10, ge=1),
        page_number: Optional[int] = Query(0, ge=0),
    ) -> None:
        self.__page_size = page_size
        self.__page_number = page_number

    @property
    def page_size(self) -> Optional[int]:
        return self.__page_size

    @property
    def page_number(self) -> Optional[int]:
        return self.__page_number


class PageResponseDto(BaseModel):
    page_size: int
    page_number: int
