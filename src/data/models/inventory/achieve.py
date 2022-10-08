from datetime import datetime

from sqlmodel import SQLModel, Field


class Achieve(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    created_at: datetime = Field(default=None)
