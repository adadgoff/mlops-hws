from typing import Type, TYPE_CHECKING

from ml_models.base import MLBaseModel
from ml_models.classification import (
    DecisionTreeClassifier,
    DecisionTreeClassifierParameters,
)
from ml_models.regression import (
    DecisionTreeRegressor,
    DecisionTreeRegressorParameters,
    LogisticRegression,
    LogisticRegressionParameters,
)


if TYPE_CHECKING:
    from core.ml_models.types import Parameters


ML_MODELS_TO_PARAMS_MAP: dict[Type[MLBaseModel], "Parameters"] = {
    # Классификация.
    DecisionTreeClassifier: DecisionTreeClassifierParameters,
    # Регрессия.
    DecisionTreeRegressor: DecisionTreeRegressorParameters,
    LogisticRegression: LogisticRegressionParameters,
}
