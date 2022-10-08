from pydantic import BaseModel


class TransactionSchema(BaseModel):
    id: int
    transaction_id: str
    transaction_status: str
