from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends
import uvicorn

from models import Author, Book, Reader, BorrowedBook, User
from models.base import Base
from models.db_helper import async_session, engine
from schemas.user import UserCreate, UserBase, UserResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@app.get("/", tags=["Home"])
def read_root():
    return {"message": "Hello, World!"}

@app.post('/register/', response_model=UserCreate)
def register(user: UserCreate):
    """Docstring"""
    return user

@app.get('/users/', response_model=UserBase)
def register(users: list[UserBase]):
    """Docstring"""
    return [user in users for user in users]

@app.get('/users/{user_id}', response_model=UserResponse)
def register(id: int, user: UserBase):
    """Docstring"""
    return user

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
