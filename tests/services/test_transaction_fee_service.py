from decimal import Decimal
from typing import Iterator

from web3 import Web3

from core.value_objects import Transaction
from services.asset_price_client import AssetPriceClient
from services.transaction_client import SwapTransactionClient
from services.transaction_fee_service import TransactionFeeService
from tests.utils.helpers import get_random_transaction


class MockSwapTransactionClient(SwapTransactionClient):
    def get_swap_transactions(self, swap_contract_address) -> Iterator[Transaction]:
        while True:
            yield get_random_transaction()

    def get_single_transaction(self, tx_hash: str) -> Transaction:
        return get_random_transaction(
            hash=tx_hash,
            gas_price=1,
            gas_used=Web3.to_wei(0.1, "ether"),
        )


class MockAssetPriceClient(AssetPriceClient):
    def get_price(self, timestamp: int) -> Decimal:
        return Decimal(1000)


def test_get_transaction_fee():
    swap_transaction_client = MockSwapTransactionClient()
    asset_price_client = MockAssetPriceClient("ETHUSDT")
    service = TransactionFeeService(swap_transaction_client, asset_price_client)
    assert service.get_transaction_fee("0x") == Decimal(100)
