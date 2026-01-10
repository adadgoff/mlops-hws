import os

from contextlib import contextmanager
from pathlib import Path

# from threading import Timer
from typing import (
    Generator,
    NamedTuple,
    Type,
)

import joblib

from core.minio import client, MINIO_ML_MODELS_BUCKET
from ml_models.base import MLBaseModel


TEMP_FOLDER = Path(
    "temp",
)


class MLModel(NamedTuple):
    ml_model: Type[MLBaseModel]
    trained: bool
    type: str


def get_created_ml_models_names() -> list[str]:
    created_ml_models_names: list[str] = [
        object_.object_name
        for object_ in client.list_objects(
            bucket_name=MINIO_ML_MODELS_BUCKET,
        )
    ]
    return created_ml_models_names


@contextmanager
def load_created_ml_model(
    created_ml_model_name: str,
) -> Generator[MLModel, None, None]:
    temp_created_ml_model_filepath = str(
        TEMP_FOLDER  # noqa.
        / created_ml_model_name
    )
    client.fget_object(
        bucket_name=MINIO_ML_MODELS_BUCKET,
        object_name=created_ml_model_name,
        file_path=temp_created_ml_model_filepath,
    )
    created_ml_model: MLModel = joblib.load(
        filename=temp_created_ml_model_filepath,
    )
    try:
        yield created_ml_model
    finally:
        os.remove(
            path=temp_created_ml_model_filepath,
        )
        # Timer(
        #     interval=2,
        #     function=lambda: os.remove(
        #         path=temp_created_ml_model_filepath,
        #     ),
        # ).start()


COMPRESS_LEVEL: int = 9


@contextmanager
def dump_ml_model(
    ml_model_name: str,
    ml_model: MLModel,
) -> Generator[None, None, None]:
    temp_ml_model_filepath = str(
        TEMP_FOLDER  # noqa.
        / ml_model_name
    )
    joblib.dump(
        value=ml_model,
        filename=temp_ml_model_filepath,
        compress=COMPRESS_LEVEL,
    )
    client.fput_object(
        bucket_name=MINIO_ML_MODELS_BUCKET,
        object_name=ml_model_name,
        file_path=temp_ml_model_filepath,
    )
    try:
        yield
    finally:
        os.remove(
            path=temp_ml_model_filepath,
        )
        # Timer(
        #     interval=2,
        #     function=lambda: os.remove(
        #         path=temp_ml_model_filepath,
        #     ),
        # ).start()
