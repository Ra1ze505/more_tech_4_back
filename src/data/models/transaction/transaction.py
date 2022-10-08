from sqlmodel import SQLModel, Field


class Transaction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    transaction_id: str
    transaction_status: str
