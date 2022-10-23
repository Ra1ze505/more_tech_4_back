from pydantic import BaseModel


class BaseSchema(BaseModel):
    ...


class OrmSchema(BaseSchema):
    class Config:
        orm_mode = True
