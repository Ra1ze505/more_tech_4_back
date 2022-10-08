from pydantic import BaseModel

from src.data.models.marketplace.admin_item import ItemType


class AdminItemBaseSchema(BaseModel):
    title: str
    description: str
    cost: int
    admin_type: ItemType

    class Config:
        orm_mode = True


class AdminItemOutSchema(AdminItemBaseSchema):
    id: int
