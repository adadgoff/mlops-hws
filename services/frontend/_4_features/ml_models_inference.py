import requests

from _6_shared.api import make_url


def inference_ml_model(
    ml_model_name: str,
    dataset_name: str,
) -> str | dict:
    response = requests.get(
        url=make_url(
            "inference",
            ml_model_name,
        ),
        params={
            "dataset_name": dataset_name,
        },
    ).json()
    return response
