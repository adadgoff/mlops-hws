import base64
import os
import requests

from pydantic import HttpUrl
from pydantic_settings import BaseSettings

from utils.api import make_url


CLEARML_WEBSERVER_API_VERSION: str = "api/v2.31"
MINIKUBE_IP: str = "192.168.200.200"


class SettingsException(Exception):
    pass


class ClearMLException(SettingsException):
    pass


class Settings(BaseSettings):
    CLEARML_WEBSERVER: HttpUrl = os.getenv(
        key="CLEARML_WEBSERVER",
        default=f"http://{MINIKUBE_IP}:30020",
    )
    CLEARML_APISERVER: HttpUrl = os.getenv(
        key="CLEARML_APISERVER",
        default=f"http://{MINIKUBE_IP}:30021",
    )
    CLEARML_FILESERVER: HttpUrl = os.getenv(
        key="CLEARML_FILESERVER",
        default=f"http://{MINIKUBE_IP}:30022",
    )
    CLEARML_USERNAME: str = os.getenv(
        key="CLEARML_USERNAME",
        default="clearml",
    )
    CLEARML_PASSWORD: str = os.getenv(
        key="CLEARML_PASSWORD",
        default="clearml123",
    )
    CLEARML_ACCESS_KEY: str | None = None
    CLEARML_SECRET_KEY: str | None = None

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

    def model_post_init(self, context):
        access_key, secret_key = self.get_clearml_credentials()
        self.CLEARML_ACCESS_KEY = access_key
        self.CLEARML_SECRET_KEY = secret_key
        return super().model_post_init(context)

    def get_clearml_authorization_header(self) -> str:
        credentials = (
            self.CLEARML_USERNAME  # noqa.
            + ":"
            + self.CLEARML_PASSWORD
        )
        encoded = base64.b64encode(
            s=credentials.encode(),
        ).decode()
        authorization_header = f"Basic {encoded}"
        return authorization_header

    def get_clearml_token(self) -> str:
        response: dict = requests.post(
            url=make_url(
                CLEARML_WEBSERVER_API_VERSION,
                "auth.login",
                base_url=self.CLEARML_WEBSERVER,
            ),
            headers={
                "authorization": self.get_clearml_authorization_header(),
            },
        ).json()
        token: str = response.get(
            "data",
            {},
        ).get(
            "token",
        )
        if token is None:
            raise ClearMLException(
                "Не удалось получить ClearML Token.",
            )
        return token

    def get_clearml_credentials(
        self,
    ) -> tuple[str, str]:
        token = self.get_clearml_token()
        response: dict = requests.post(
            url=make_url(
                CLEARML_WEBSERVER_API_VERSION,
                "auth.create_credentials",
                base_url=self.CLEARML_WEBSERVER,
            ),
            headers={
                "cookie": f"clearml-token-k8s={token}",
            },
        ).json()
        credentials: dict = response.get(
            "data",
            {},
        ).get(
            "credentials",
        )
        if credentials is None:
            raise ClearMLException(
                "Не удалось получить ClearML Credentials.",
            )
        access_key = credentials.get("access_key")
        secret_key = credentials.get("secret_key")
        if access_key is None:
            raise ClearMLException(
                "Не удалось получить ClearML access_key.",
            )
        if secret_key is None:
            raise ClearMLException(
                "Не удалось получить ClearML secret_key.",
            )
        return access_key, secret_key


settings = Settings()
