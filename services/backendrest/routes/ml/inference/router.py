import os

from threading import Timer

import pandas as pd

from clearml import (
    Task,
    TaskTypes,
)
from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from core.clearml import CLEARML_PROJECT_NAME
from core.datasets.consts import (
    DATASET_ALLOWED_EXTENSION,
    DATASET_TARGET_COLUMN,
)
from core.dvc import (
    dvc_file_system,
    DVC_FOLDER,
    dvc_temp_from_remote_manager,
)
from core.ml_models.s3_manager import (
    get_created_ml_models_names,
    load_created_ml_model,
)
from utils.api import URL_DELIMITER


router = APIRouter(
    prefix="/inference",
    tags=["ML Models", "ML Models Inference"],
)


@router.get(
    path="/{ml_model_name}",
    summary="Получить инференс у выбранной по имени модели.",
)
async def get_inference(
    ml_model_name: str,
    dataset_name: str,
) -> str:
    if ml_model_name not in set(
        get_created_ml_models_names(),
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ML модель с именем {ml_model_name} не существует.",
        )
    if not dvc_file_system.exists(
        dataset_name=dataset_name,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Датасет с именем {dataset_name} не существует.",
        )
    with (
        load_created_ml_model(
            created_ml_model_name=ml_model_name,
        ) as created_ml_model,
        dvc_temp_from_remote_manager(
            dataset_name=dataset_name,
        ) as temp_datasets_filepath,
    ):
        if created_ml_model.trained is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"ML модель {ml_model_name} не обучена"
                    + " "
                    + "и не готова к инференсу."
                ),
            )
        df = pd.read_csv(
            filepath_or_buffer=temp_datasets_filepath,
        )
        target_column = next(
            (
                column  # noqa.
                for column in df.columns
                if column.lower() == DATASET_TARGET_COLUMN
            ),
            None,
        )
        if target_column is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Столбец `target` не должен быть"
                    + " "
                    + f"в датасете {dataset_name} для инференса."
                ),
            )
        task = Task.init(
            project_name=CLEARML_PROJECT_NAME,
            task_name=f"inference-{ml_model_name}-{dataset_name}",
            task_type=TaskTypes.inference,
        )
        task.connect(
            created_ml_model.ml_model.get_params(),
        )
        df["Predictions"] = created_ml_model.ml_model.predict(
            df,
        )
        df_temp_filepath = str(
            DVC_FOLDER
            / (
                dataset_name.rstrip(DATASET_ALLOWED_EXTENSION)
                + "_with_predictions"
                + DATASET_ALLOWED_EXTENSION
            )
        )
        df.to_csv(
            path_or_buf=df_temp_filepath,
        )
        dvc_file_system.put_file(
            lpath=df_temp_filepath,
        )
        Timer(
            interval=2,
            function=lambda: os.remove(
                path=df_temp_filepath,
            ),
        ).start()
        return df_temp_filepath.lstrip(
            str(DVC_FOLDER) + URL_DELIMITER,
        )
