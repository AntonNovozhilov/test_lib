from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.auth import auth_router
from api.book import book
from api.borrow import borrow
from api.reader import reader
from models.base import Base
from models.db_helper import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(book)
app.include_router(reader)
app.include_router(borrow)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
