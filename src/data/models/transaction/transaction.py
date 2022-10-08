from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):
    id: int = Field(primary_key=True)
    transaction_id: str
    transaction_status: str
