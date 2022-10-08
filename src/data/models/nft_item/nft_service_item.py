from sqlmodel import SQLModel, Field


class NFTServiceItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nft_id: str
    item_id: int = Field(foreign_key="admin_item.id")
