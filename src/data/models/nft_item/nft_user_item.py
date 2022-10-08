from sqlmodel import Field, SQLModel


class NFTUserItem(SQLModel, table=True):
    id: int = Field(primary_key=True)
    nft_id: str
    item_id: int = Field(foreign_key="event.id")
