from sqlmodel import Field, SQLModel


class Quest(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    description: str
    reward: int
