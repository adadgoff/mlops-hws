from typing import Type

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import BaseModel
from pydantic.alias_generators import to_snake


from core.minio import client, MINIO_ML_MODELS_BUCKET
from core.ml_models.maps import ML_MODELS_TO_PARAMS_MAP
from core.ml_models.s3_manager import (
    get_created_ml_models_names,
    dump_ml_model,
    load_created_ml_model,
    MLModel,
)
from ml_models.base import MLBaseModel
from routes.ml.crud.exceptions import UnknownMLModelException
from routes.ml.crud.schemas import (
    CreatedMLModelSchema,
    MLModelSchema,
    TrainedMLModelSchema,
)


router = APIRouter(
    prefix="/mlmodels",
    tags=["ML Models", "ML Models CRUD"],
)


@router.get(
    path="",
    summary="Получить список доступных моделей.",
)
async def get_ml_models() -> list[MLModelSchema]:
    ml_models: list[MLModelSchema] = []
    for ml_model, parameters in ML_MODELS_TO_PARAMS_MAP.items():
        ml_models.append(
            MLModelSchema(
                type=ml_model.__name__,
                parameters=parameters(),
            )
        )
    return ml_models


@router.get(
    path="/created",
    summary="Получить список созданных моделей.",
)
async def get_created_ml_models() -> list[CreatedMLModelSchema]:
    created_ml_models: list[CreatedMLModelSchema] = []

    for created_ml_model_name in get_created_ml_models_names():
        with load_created_ml_model(
            created_ml_model_name=created_ml_model_name,
        ) as created_ml_model:
            created_ml_models.append(
                CreatedMLModelSchema(
                    name=created_ml_model_name,
                    type=created_ml_model.type,
                    trained=created_ml_model.trained,
                    parameters=created_ml_model.ml_model.get_params(),
                )
            )

    return created_ml_models


@router.get(
    path="/trained",
    summary="Получить список обученных моделей.",
)
async def get_trained_ml_models() -> list[TrainedMLModelSchema]:
    trained_ml_models: list[TrainedMLModelSchema] = []

    for created_ml_model_name in get_created_ml_models_names():
        with load_created_ml_model(
            created_ml_model_name=created_ml_model_name,
        ) as created_ml_model:
            if created_ml_model.trained is True:
                trained_ml_models.append(
                    TrainedMLModelSchema(
                        name=created_ml_model_name,
                        type=created_ml_model.type,
                        parameters=created_ml_model.ml_model.get_params(),
                    )
                )

    return trained_ml_models


def create_ml_model_endpoint(
    ml_model: Type[MLBaseModel],
    parameters: Type[BaseModel],
):
    async def wrapper(
        ml_model_name: str = Body(
            ...,
            description="Имя создаваемой модели",
        ),
        parameters: parameters = Body(
            ...,
            description="Параметры модели",
        ),
    ) -> str:
        if ml_model_name in set(
            get_created_ml_models_names(),
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"ML модель с именем {ml_model_name} уже существует.",
            )
        with dump_ml_model(
            ml_model_name=ml_model_name,
            ml_model=MLModel(
                ml_model=ml_model(**parameters.model_dump()),
                trained=False,
                type=ml_model.__name__,
            ),
        ):
            return ml_model_name

    return wrapper


for ml_model in ML_MODELS_TO_PARAMS_MAP.keys():
    parameters = ML_MODELS_TO_PARAMS_MAP.get(ml_model)
    if parameters is None:
        raise UnknownMLModelException(f"Неизвестная модель: {ml_model}.")

    router.add_api_route(
        path=f"/create/{to_snake(ml_model.__name__)}",
        endpoint=create_ml_model_endpoint(
            ml_model,
            parameters,
        ),
        methods=["POST"],
        response_description="Имя созданной модели",
        summary=f"Создать {ml_model.__name__} модель.",
    )


@router.delete(
    path="/delete/{ml_model_name}",
    summary="Удалить модель машинного обучения по имени.",
)
async def delete_ml_model(
    ml_model_name: str,
) -> str:
    if ml_model_name not in set(
        get_created_ml_models_names(),
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ML модель с именем {ml_model_name} не существует.",
        )
    client.remove_object(
        bucket_name=MINIO_ML_MODELS_BUCKET,
        object_name=ml_model_name,
    )
    return ml_model_name
