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
from core.datasets.consts import DATASET_TARGET_COLUMN
from core.dvc import (
    dvc_file_system,
    dvc_temp_from_remote_manager,
)
from core.ml_models.s3_manager import (
    dump_ml_model,
    get_created_ml_models_names,
    load_created_ml_model,
    MLModel,
)
from routes.ml.train.schemas import TrainedMLModel


router = APIRouter(
    prefix="/train",
    tags=["ML Models", "ML Models Train"],
)


@router.post(
    path="/{ml_model_name}",
    summary="""
        Обучить выбранную по имени модель
        на выбранном по имени датасете.
    """,
)
async def train_model(
    ml_model_name: str,
    dataset_name: str,
) -> TrainedMLModel:
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
        if target_column is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Столбец `target` не найден"
                    + " "
                    + f"в датасете {dataset_name} для обучения."
                ),
            )
        task = Task.init(
            project_name=CLEARML_PROJECT_NAME,
            task_name=f"train-{ml_model_name}-{dataset_name}",
            task_type=TaskTypes.training,
        )
        task.connect(
            created_ml_model.ml_model.get_params(),
        )
        X = df.drop(columns=[target_column])
        y = df[target_column]
        created_ml_model.ml_model.fit(
            X,
            y,
        )
    with dump_ml_model(
        ml_model_name=ml_model_name,
        ml_model=MLModel(
            ml_model=created_ml_model.ml_model,
            trained=True,
            type=created_ml_model.type,
        ),
    ):
        return TrainedMLModel(
            ml_model_name=ml_model_name,
            dataset_name=dataset_name,
        )
