import enum

from sqlmodel import Column, Enum, Field, SQLModel


class ItemType(str, enum.Enum):
    reaction = "reaction"
    medal = "medal"


class AdminItem(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    description: str
    cost: int
    admin_type: ItemType = Field(sa_column=Column(Enum(ItemType)), default=ItemType.reaction)
