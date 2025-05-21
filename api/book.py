from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.book import Book
from models.db_helper import get_session
from schemas.books import BookCreat, BookResponse


book = APIRouter()

@book.post('/book/', tags=['Books'], status_code=201, response_model=BookCreat)
async def bookcreat(book: BookCreat, db: AsyncSession = Depends(get_session)):
    """Docstring"""
    new_book = db.add(Book(**book.model_dump()))
    await db.commit()
    await db.refresh(new_book)
    return new_book
