from sqlmodel import SQLModel, Field


class NFTServiceItem(SQLModel, table=True):
    id: int = Field(primary_key=True)
    nft_id: str
    item_id: int = Field(foreign_key="adminitem.id")
