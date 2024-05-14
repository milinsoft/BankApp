from pydantic import BaseModel


class ModelSchema(BaseModel):
    class Config:  # noqa: D105,D106
        from_attributes = True
