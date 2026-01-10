import requests

from streamlit.runtime.uploaded_file_manager import UploadedFile

from _5_entities import Dataset
from _6_shared.api import (
    make_url,
    OK_STATUS,
)


DATASETS_URL = make_url(
    "datasets",
)


class DatasetException(Exception):
    pass


def get_datasets() -> list[Dataset]:
    response = requests.get(
        url=DATASETS_URL,
    ).json()
    return [
        Dataset.model_validate(dataset)  # noqa.
        for dataset in response
    ]


def upload_dataset(
    dataset_name: str,
    dataset_file: UploadedFile,
) -> str | dict:
    response = requests.post(
        url=make_url(
            "upload",
            base_url=DATASETS_URL,
        ),
        files={
            "dataset_name": (
                None,
                dataset_name,
            ),
            "dataset_file": (
                dataset_file.name,
                dataset_file.getvalue(),
                dataset_file.type,
            ),
        },
        headers={
            "accept": "application/json",
        },
    ).json()
    return response


def download_dataset(
    dataset_name: str,
) -> str:
    response = requests.get(
        url=make_url(
            "download",
            dataset_name,
            base_url=DATASETS_URL,
        ),
    )
    if response.status_code == OK_STATUS:
        return response.content.decode(
            encoding="utf-8",
        )
    raise DatasetException(
        f"Датасет {dataset_name} не найден.",
    )


def delete_dataset(
    dataset_name: str,
) -> str | dict:
    response = requests.delete(
        url=make_url(
            "delete",
            dataset_name,
            base_url=DATASETS_URL,
        ),
    ).json()
    return response
