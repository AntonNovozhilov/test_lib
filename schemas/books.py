from pydantic import BaseModel, Field
from typing import Optional


class BookBase(BaseModel):
    """Docstring"""
    title: str
    author: str
    year: Optional[int]
    isbn: Optional[str]
    count: int = Field(default=1, ge=0)


class BookCreat(BookBase):
    pass

class BookResponse(BookBase):
    id: int


    class Config:
        orm_mode = True
