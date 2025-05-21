from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings



engine = create_async_engine(
        url=settings.db_url,
        echo=True,
    )


async_session = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False
    )
