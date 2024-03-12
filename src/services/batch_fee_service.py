import time

from models import ImportingJob, Transaction
from services.transaction_client import SwapTransactionClient
from services.transaction_fee_service import TransactionFeeService


class BatchFeeService:
    def __init__(
        self,
        swap_transaction_client: SwapTransactionClient,
        transaction_fee_service: TransactionFeeService,
    ) -> None:
        self.swap_transaction_client = swap_transaction_client
        self.transaction_fee_service = transaction_fee_service

    def get_batch_transactions(self, importing_job: ImportingJob) -> list[Transaction]:
        print("Getting transactions")
        transactions = self.swap_transaction_client.get_swap_transactions(
            swap_contract_address="0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
            block_window=importing_job.block_window,
        )
        for idx, transaction in enumerate(transactions):
            self.transaction_fee_service.get_transaction_fee(transaction.tx_hash)
            if idx % 20 == 0:  # Commit every 20 transactions
                importing_job.last_block_processed = transaction.block_number
                self.transaction_fee_service.session.add(importing_job)
                self.transaction_fee_service.session.commit()
            time.sleep(0.1)  # Avoid rate limiting
        importing_job.last_block_processed = importing_job.end_block_number
        self.transaction_fee_service.session.add(importing_job)
        return list(transactions)
