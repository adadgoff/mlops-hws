from pydantic import HttpUrl


URL_DELIMITER: str = "/"


def make_url(
    *paths: str,
    base_url: HttpUrl,
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
