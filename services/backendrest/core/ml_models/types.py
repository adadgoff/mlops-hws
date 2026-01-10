from typing import Union

from core.ml_models.maps import (
    ML_MODELS_TO_PARAMS_MAP,
)


Parameters = Union[*ML_MODELS_TO_PARAMS_MAP.values()]
