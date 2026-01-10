import requests

from pydantic.alias_generators import to_snake

from _5_entities import (
    CreatedMLModel,
    MLModel,
    TrainedMLModel,
)
from _6_shared.api import make_url
from _6_shared.types import Parameters


ML_MODELS_URL = make_url(
    "mlmodels",
)


def get_ml_models() -> list[MLModel]:
    response = requests.get(
        url=ML_MODELS_URL,
    ).json()
    return [
        MLModel.model_validate(ml_model)  # noqa.
        for ml_model in response
    ]


def get_created_ml_models() -> list[CreatedMLModel]:
    response = requests.get(
        url=make_url(
            "created",
            base_url=ML_MODELS_URL,
        ),
    ).json()
    return [
        CreatedMLModel.model_validate(created_ml_model)  # noqa.
        for created_ml_model in response
    ]


def get_trained_ml_models() -> list[TrainedMLModel]:
    response = requests.get(
        url=make_url(
            "trained",
            base_url=ML_MODELS_URL,
        )
    ).json()
    return [
        TrainedMLModel.model_validate(trained_ml_model)  # noqa.
        for trained_ml_model in response
    ]


def create_ml_model(
    *,
    ml_model_name: str,
    ml_model_type: str,
    parameters: Parameters,
) -> str | dict:
    response = requests.post(
        url=make_url(
            "create",
            to_snake(ml_model_type),
            base_url=ML_MODELS_URL,
        ),
        json={
            "ml_model_name": ml_model_name,
            "parameters": parameters,
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
    ).json()
    return response


def delete_ml_model(
    ml_model_name: str,
) -> str | dict:
    response = requests.delete(
        url=make_url(
            "delete",
            ml_model_name,
            base_url=ML_MODELS_URL,
        ),
    ).json()
    return response
