from routes.datasets import datasets_router
from routes.health import health_router
from routes.ml import (
    ml_inference_router,
    ml_crud_router,
    ml_train_router,
)


__all__ = [
    "datasets_router",
    "health_router",
    "ml_inference_router",
    "ml_crud_router",
    "ml_train_router",
]
