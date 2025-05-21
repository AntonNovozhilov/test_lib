from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
import uvicorn

from models import Book, Reader, BorrowedBook, User
from models.base import Base
from models.db_helper import engine
from schemas.user import UserCreate
from api.auth import auth_router
from api.book import book

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(book)

@app.get("/", tags=["Home"])
def read_root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
