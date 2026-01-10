from pydantic import BaseModel


class DatasetSchema(BaseModel):
    name: str
    size: str
