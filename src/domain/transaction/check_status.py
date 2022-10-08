from src.data.repos.polygon.transfer import TransferApiRepo
from src.data.repos.transaction import TransactionRepo


class CheckStatusUseCase:
    def __init__(self, transaction_repo: TransactionRepo, transfer_repo: TransferApiRepo):
        self.transaction_repo = transaction_repo
        self.transfer_repo = transfer_repo

    async def __call__(self):
        transactions = await self.transaction_repo.get_for_check_status()
        for transaction in transactions:
            status = await self.transfer_repo.transfer_status(transaction.transaction_hash)
            if status.get("status") == "Success":
                await self.transaction_repo.update(
                    {"id": transaction.id, "transaction_status": "completed"}
                )
