from sqlmodel import SQLModel, Field


class Quest(SQLModel, table=True):
    id: int = Field( primary_key=True)
    title: str
    description: str
    reward: int
