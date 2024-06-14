from pydantic import BaseModel, ConfigDict


class ModelSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
