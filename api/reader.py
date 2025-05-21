from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import get_current_user
from models.db_helper import get_session
from models.reader import Reader
from schemas.reads import ReaderCreate, ReaderResponse, ReaderUpdate

reader = APIRouter(prefix="/reader", tags=["Readers"])


@reader.post("/", response_model=ReaderCreate, status_code=HTTPStatus.CREATED)
async def create_reader(
    reader: ReaderCreate,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """Docstring"""
    reader_unit = await db.execute(select(Reader).where(Reader.email == reader.email))
    db_reader = reader_unit.scalars().first()
    if db_reader:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Пользователь с такими данными уже есть в системе.",
        )
    new_reader = Reader(**reader.model_dump())
    db.add(new_reader)
    await db.commit()
    await db.refresh(new_reader)
    return new_reader


@reader.get("/", response_model=list[ReaderResponse])
async def list_readers(
    db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)
):
    """Docstring"""
    result = await db.execute(select(Reader))
    return result.scalars().all()


@reader.get("/{reader_id}", response_model=ReaderResponse)
async def get_reader(
    reader_id: int,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """Docstring"""
    reader_unit = await db.execute(select(Reader).where(Reader.id == reader_id))
    db_reader = reader_unit.scalars().first()
    if not db_reader:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Пользователь с такими данными не найден.",
        )
    return db_reader


@reader.put("/{reader_id}", response_model=ReaderResponse)
async def update_reader(
    reader_id: int,
    data: ReaderUpdate,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """Docstring"""
    reader_unit = await db.execute(select(Reader).where(Reader.id == reader_id))
    db_reader = reader_unit.scalars().first()
    if not db_reader:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Пользователь с такими данными не найден.",
        )
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_reader, key, value)
    await db.commit()
    await db.refresh(db_reader)
    return db_reader


@reader.delete("/{reader_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_reader(
    reader_id: int,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """Docstring"""
    reader_unit = await db.execute(select(Reader).where(Reader.id == reader_id))
    db_reader = reader_unit.scalars().first()
    if not db_reader:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Пользователь с такими данными не найден.",
        )
    await db.delete(db_reader)
    await db.commit()
