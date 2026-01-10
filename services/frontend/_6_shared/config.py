import os

from pydantic import HttpUrl
from pydantic_settings import (
    BaseSettings,
)


class Settings(BaseSettings):
    BACKEND_ADDRESS: HttpUrl = os.getenv(
        key="BACKEND_ADDRESS",
        default="http://localhost:8000",
    )


settings = Settings()
