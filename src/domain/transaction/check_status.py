from src.data.repos.polygon.transfer import TransferApiRepo
from src.data.repos.transaction import TransactionRepo
from src.domain.transaction.dto import TransactionSchema


class CheckStatusUseCase:
    def __init__(self, transaction_repo: TransactionRepo, transfer_repo: TransferApiRepo):
        self.transaction_repo = transaction_repo
        self.transfer_repo = transfer_repo

    async def __call__(self):
        transactions: list[TransactionSchema] = await self.transaction_repo.get_for_check_status()
        for transaction in transactions:
            status = await self.transfer_repo.transfer_status(transaction.transaction_id)
            await self.transaction_repo.update(
                {"id": transaction.id, "transaction_status": status.get("status")}
            )
