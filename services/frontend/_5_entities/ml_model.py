from pydantic import BaseModel


class MLModel(BaseModel):
    type: str
    parameters: dict


class TrainedMLModel(MLModel):
    name: str


class CreatedMLModel(TrainedMLModel):
    trained: bool
