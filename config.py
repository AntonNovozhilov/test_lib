import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_driver = os.getenv("DB_DRIVER")


class Setting(BaseSettings):
    db_url: str = f"{db_driver}://{db_user}:{db_password}@{db_host}:{db_host}/{db_name}"


settings = Setting()
