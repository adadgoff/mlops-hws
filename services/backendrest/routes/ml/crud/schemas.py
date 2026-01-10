from pydantic import BaseModel

from core.ml_models.types import Parameters


class MLModelSchema(BaseModel):
    type: str
    parameters: Parameters


class TrainedMLModelSchema(MLModelSchema):
    name: str


class CreatedMLModelSchema(TrainedMLModelSchema):
    trained: bool
