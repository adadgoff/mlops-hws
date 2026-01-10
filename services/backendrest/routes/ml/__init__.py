from routes.ml.crud import ml_crud_router
from routes.ml.inference import ml_inference_router
from routes.ml.train import ml_train_router

__all__ = [
    "ml_crud_router",
    "ml_inference_router",
    "ml_train_router",
]
