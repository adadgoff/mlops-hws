from pydantic import HttpUrl

from _6_shared.config import settings


OK_STATUS: int = 200

URL_DELIMITER: str = "/"


def make_url(
    *paths: str,
    base_url: HttpUrl = settings.BACKEND_ADDRESS,
) -> str:
    base_url = str(base_url).rstrip(URL_DELIMITER)
    paths = (
        path.strip(URL_DELIMITER)  # noqa.
        for path in paths
    )
    url = (
        base_url  # noqa.
        + URL_DELIMITER
        + URL_DELIMITER.join(paths)
    )
    return url


DOCS_URL: str = make_url("docs")
REDOC_BACKEND_ADDRESS: str = make_url("redoc")
