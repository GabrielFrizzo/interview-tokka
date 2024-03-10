from decimal import Decimal

from services.asset_price_client import AssetPriceClient
from services.transaction_client import TransactionClient


class TransactionFeeService:
    def __init__(
        self,
        transaction_client: TransactionClient,
        asset_price_client: AssetPriceClient,
    ) -> None:
        self.transaction_client = transaction_client
        self.asset_price_client = asset_price_client

    def get_transaction_fee(self, address: str) -> Decimal:
        tx = self.transaction_client.get_single_transaction(address)
        eth_price = self.asset_price_client.get_price(tx.time_stamp)

        return tx.get_eth_used() * eth_price
