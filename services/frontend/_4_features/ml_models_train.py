import requests

from requests import Response

from _6_shared.api import make_url


def train_ml_model(
    ml_model_name: str,
    dataset_name: str,
) -> Response:
    response = requests.post(
        url=make_url(
            "train",
            ml_model_name,
        ),
        params={
            "dataset_name": dataset_name,
        },
    )
    return response
