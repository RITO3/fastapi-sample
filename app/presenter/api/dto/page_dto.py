from pydantic import BaseModel, Field
from fastapi import Query


class PageQueryParameterDto:
    def __init__(
        self,
        page_size: int = Query(10, title="ページサイズ", description="ページサイズ", ge=10),
        page_number: int = Query(1, title="ページ番号", description="ページ番号", ge=1),
    ) -> None:
        self.__page_size = page_size
        self.__page_number = page_number

    @property
    def page_size(self) -> int:
        return self.__page_size

    @property
    def page_number(self) -> int:
        return self.__page_number


class PageResponseDto(BaseModel):
    page_size: int = Field(..., title="ページサイズ", description="ページサイズ")
    page_number: int = Field(..., title="ページ番号", description="ページ番号")
