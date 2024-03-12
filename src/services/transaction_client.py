from abc import ABC, abstractmethod
from typing import Iterator

from models import BlockWindow, Transaction


class TransactionClient(ABC):
    @abstractmethod
    def get_single_transaction(self, tx_hash: str) -> Transaction:
        pass


class SwapTransactionClient(ABC):
    @abstractmethod
    def get_swap_transactions(
        self, swap_contract_address: str, block_window: BlockWindow
    ) -> Iterator[Transaction]:
        pass
