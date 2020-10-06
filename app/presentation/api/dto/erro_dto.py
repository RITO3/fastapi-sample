from typing import List

from pydantic import BaseModel, Field


class BadRequestParameter(BaseModel):
    name: str = Field(..., title="パラメータ名", description="パラメータ名")
    message: str = Field(..., title="メッセージ", description="メッセージ")


class BadRequestDto(BaseModel):
    message: str = Field(..., title="メッセージ", description="メッセージ")
    parameters: List[BadRequestParameter] = Field(
        ..., title="パラメータ", description="パラメータ"
    )
