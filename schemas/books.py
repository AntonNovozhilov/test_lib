from typing import Optional

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    """Docstring"""

    title: str
    author: str
    year: Optional[int]
    isbn: Optional[str]
    count: int = Field(default=1, ge=0)
    description: str


class BookCreat(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookResponse(BookBase):
    id: int

    class Config:
        orm_mode = True
