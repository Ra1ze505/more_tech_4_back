from sqlmodel import SQLModel, Field


class CountMedalUser(SQLModel):
    gold: int
    silver: int
    bronze: int


class Inventory(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    list_achieve: list[int]
    list_nft_user_item: list[int]
    list_nft_reaction: list[int]
    count_medal_user: CountMedalUser
