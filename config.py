from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    db_url: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/test_lib'

settings = Setting()
