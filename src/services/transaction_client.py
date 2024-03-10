from abc import ABC, abstractmethod
from typing import Iterator

from core.value_objects import Transaction


class SwapTransactionClient(ABC):
    @abstractmethod
    def get_swap_transactions(self, swap_contract_address: str) -> Iterator[Transaction]:
        pass

    @abstractmethod
    def get_single_transaction(self, tx_hash: str) -> Transaction:
        pass
