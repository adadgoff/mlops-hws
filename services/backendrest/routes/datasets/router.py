import os

from typing import Annotated

import numpy as np
import pandas as pd
from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    status,
    UploadFile,
)
from fastapi.responses import FileResponse

from core.dvc import (
    DVC_FOLDER,
    dvc_file_system,
    dvc_temp_from_local_manager,
    dvc_temp_from_remote_manager,
)
from core.datasets.consts import (
    DATASET_ALLOWED_EXTENSION,
    DATASET_TARGET_COLUMN,
)
from routes.datasets.schemas import DatasetSchema
from routes.datasets.utils import verify_dataset_name


router = APIRouter(
    tags=["Datasets"],
    prefix="/datasets",
)


@router.get(
    path="",
    summary="Получить список датасетов.",
)
async def get_datasets() -> list[DatasetSchema]:
    return dvc_file_system.ls()


@router.get(
    path="/download/{dataset_name}",
    summary="Скачать датасет по названию.",
)
async def download_dataset(
    dataset_name: str,
) -> FileResponse:
    if not dvc_file_system.exists(dataset_name=dataset_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Датасет с именем {dataset_name} не существует.",
        )
    with dvc_temp_from_remote_manager(
        dataset_name=dataset_name,
    ) as temp_dataset_filepath:
        return FileResponse(
            path=temp_dataset_filepath,
            filename=dataset_name,
            media_type="text/cvs",
        )


@router.post(
    path="/upload",
    summary="Загрузить датасет.",
)
async def upload_dataset(
    dataset_name: Annotated[str, Body()],
    dataset_file: UploadFile,
) -> str:
    if not verify_dataset_name(dataset_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Некорректное название датасета."
                + " "
                + "Используйте латинские буквы, цифры и нижнее подчеркивание."
            ),
        )
    dataset_name += DATASET_ALLOWED_EXTENSION
    if dvc_file_system.exists(dataset_name=dataset_name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Датасет с именем {dataset_name} уже существует.",
        )
    _, dataset_file_extension = os.path.splitext(dataset_file.filename)
    if dataset_file_extension != DATASET_ALLOWED_EXTENSION:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Некорректное расширение файла датасета."
                + " "
                + "Загружайте только файлы с расширением"
                + DATASET_ALLOWED_EXTENSION
                + "."
            ),
        )
    async with dvc_temp_from_local_manager(
        dataset_name=dataset_name,
        dataset_file=dataset_file,
    ) as temp_dataset_filepath:
        df = pd.read_csv(
            filepath_or_buffer=temp_dataset_filepath,
        )
        non_numeric_columns = df.select_dtypes(
            exclude=[np.number],
        ).columns
        if len(non_numeric_columns) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Датасет содержит нечисловые столбцы: "
                    + ", ".join(non_numeric_columns)
                    + "."
                ),
            )
        dvc_file_system.put_file(
            lpath=temp_dataset_filepath,
        )
        return dataset_name


@router.delete(
    path="/delete/{dataset_name}",
    summary="Удалить датасет по названию.",
)
async def delete_dataset(
    dataset_name: str,
) -> str:
    if not dvc_file_system.exists(dataset_name=dataset_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Датасет с именем {dataset_name} не существует.",
        )
    dvc_file_system.rm(
        path=str(DVC_FOLDER / dataset_name),
    )
    return dataset_name
