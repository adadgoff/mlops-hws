from clearml import Task

from core.config import settings


CLEARML_PROJECT_NAME: str = "MLOps-HW1"


def setup_clearml_credentials():
    Task.set_credentials(
        api_host=settings.CLEARML_APISERVER,
        web_host=settings.CLEARML_WEBSERVER,
        files_host=settings.CLEARML_FILESERVER,
        key=settings.CLEARML_ACCESS_KEY,
        secret=settings.CLEARML_SECRET_KEY,
    )
