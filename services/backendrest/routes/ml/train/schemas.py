from pydantic import BaseModel


class TrainedMLModel(BaseModel):
    ml_model_name: str
    dataset_name: str
