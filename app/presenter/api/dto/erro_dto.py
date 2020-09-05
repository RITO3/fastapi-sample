from typing import List
from pydantic import BaseModel


class BadRequestParameter(BaseModel):
    name: str
    message: str


class BadRequestDto(BaseModel):
    message: str
    parameters: List[BadRequestParameter]
