from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BorrowBook(BaseModel):
    id: int
    book_id: int
    reader_id: int
    borrowed_date: datetime
    return_date: Optional[datetime]


class BorrowBookResponse(BaseModel):
    book_id: int
    reader_id: int

    class Config:
        orm_mode = True
