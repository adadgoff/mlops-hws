import os

from pydantic_settings import BaseSettings


MINIKUBE_IP: str = "192.168.200.200"


class Settings(BaseSettings):
    MINIO_CONSOLE: str = os.getenv(
        key="MINIO_CONSOLE",
        default=f"{MINIKUBE_IP}:30031",
    )
    MINIO_ACCESS_KEY: str = os.getenv(
        key="MINIO_ACCESS_KEY",
        default="minio",
    )
    MINIO_SECRET_KEY: str = os.getenv(
        key="MINIO_SECRET_KEY",
        default="minio123",
    )


settings = Settings()
