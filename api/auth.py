from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import authenticate_user, create_access_token, get_password_hash
from models.db_helper import get_session
from models.user import User
from schemas.user import UserCreate

auth_router = APIRouter()


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_session)):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()


@auth_router.post("/register/", tags=["Auth"], response_model=UserCreate)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    """Docstring"""
    get_user = await get_user_by_email(email=user.email, db=db)
    if get_user:
        raise HTTPException(
            detail="Пользователь с указанной почтой уже зарегистрирован.",
            status_code=HTTPStatus.CONFLICT,
        )
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@auth_router.post("/login/", tags=["Auth"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(
        db=db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            detail="Пароль или почта недействительны.", status_code=HTTPStatus.CONFLICT
        )
    acces_token = create_access_token(data={"sub": user.email})
    return {"acces_token": acces_token, "token_type": "bearer"}
