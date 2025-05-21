from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Borrow(BaseModel):
    book_id: int
    reader_id: int
    borrow_date: datetime
    return_date: Optional[str]

    class Config:
        orm_mode = True