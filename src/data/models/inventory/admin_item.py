import enum

from sqlmodel import SQLModel, Field, Enum, Column


class ItemType(str, enum.Enum):
    reaction = "reaction"
    medal = "medal"


class AdminItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    cost: int
    admin_type: ItemType = Field(sa_column=Column(Enum(ItemType)), default=ItemType.reaction)
