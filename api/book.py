from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import get_current_user
from models.book import Book
from models.db_helper import get_session
from schemas.books import BookCreat, BookResponse, BookUpdate

book = APIRouter(prefix="/books", tags=["Books"])


@book.get("/", response_model=list[BookResponse])
async def get_books_list(
    db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)
):
    result = await db.execute(select(Book))
    books = result.scalars().all()
    return books


@book.post("/", status_code=HTTPStatus.CREATED, response_model=BookCreat)
async def book_creat(
    book: BookCreat,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """Docstring"""
    book_unit = await db.execute(select(Book).where(Book.isbn == book.isbn))
    if book_unit.scalars().first():
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Книга с таки sbin уже есть в системе.",
        )
    book_unit_id = await db.execute(select(Book).where(Book.id == book.id))
    if book_unit_id.scalars().first():
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Книга с таким ID уже существует."
        )
    db_book = Book(**book.model_dump())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book


@book.get("/{book_id}", response_model=BookResponse)
async def read_book(
    book_id: int,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalars().first()
    if not result.scalars().first():
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Книга не найдена")
    return db_book


@book.put("/{book_id}", response_model=BookCreat)
async def update_book(
    book_id: int,
    book: BookUpdate,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalars().first()
    if not db_book:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Книга не найдена")
    update_data = book.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    await db.commit()
    await db.refresh(db_book)
    return db_book


@book.delete("/{book_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalars().first()
    if not db_book:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Книга не найдена")
    await db.delete(db_book)
    await db.commit()
