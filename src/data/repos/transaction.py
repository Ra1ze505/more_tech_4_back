from pydantic import parse_obj_as
from sqlalchemy import select

from src.data.models import Transaction
from src.data.repos.base import BaseRepo
from src.domain.transaction.dto import TransactionSchema


class TransactionRepo(BaseRepo):

    model = Transaction
    schema = TransactionSchema

    async def get_for_check_status(self) -> list[TransactionSchema]:
        q = select(self.model).where(self.model.transaction_status != "Success")
        transactions = (await self.session.execute(q)).scalars().all()
        return [parse_obj_as(self.schema, t) for t in transactions]
