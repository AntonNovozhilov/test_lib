from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import get_current_user
from models.book import Book
from models.borrowedbooks import BorrowedBook
from models.db_helper import get_session
from models.reader import Reader
from schemas.books import BookResponse
from schemas.borrow import BorrowBook, BorrowBookResponse

borrow = APIRouter(tags=["Borrows"])


@borrow.post("/borrow/", response_model=BorrowBook, status_code=HTTPStatus.CREATED)
async def borrow_book(
    data: BorrowBookResponse,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """Docstring"""
    book = await db.get(Book, data.book_id)
    result = await db.execute(
        select(func.count(BorrowedBook.id)).where(
            and_(
                BorrowedBook.reader_id == data.reader_id,
                BorrowedBook.return_date.is_(None),
            )
        )
    )
    active_borrows = result.scalar()
    if active_borrows >= 3:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="У читателя уже 3 книги на руках"
        )
    borrowed = BorrowedBook(book_id=data.book_id, reader_id=data.reader_id)
    book.count -= 1
    db.add(borrowed)
    await db.commit()
    await db.refresh(borrowed)
    return borrowed


@borrow.get("/borrow/{reader_id}", response_model=list[BookResponse])
async def books_one_reader(
    reader_id: int,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """Docstring"""
    result = await db.execute(
        select(Book)
        .join(BorrowedBook)
        .where(BorrowedBook.reader_id == reader_id, BorrowedBook.return_date.is_(None))
    )
    books = result.scalars().all()
    return books


@borrow.post("/return/", response_model=BorrowBook)
async def return_book(
    data: BorrowBookResponse,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    result = await db.execute(
        select(BorrowedBook).where(
            and_(
                BorrowedBook.book_id == data.book_id,
                BorrowedBook.reader_id == data.reader_id,
                BorrowedBook.return_date.is_(None),
            )
        )
    )
    borrowed = result.scalars().first()
    if not borrowed:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Книга не была выдана"
        )
    borrowed.return_date = datetime.now()
    book = await db.get(Book, data.book_id)
    book.count += 1
    await db.commit()
    await db.refresh(borrowed)
    return borrowed
