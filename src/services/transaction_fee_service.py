from decimal import Decimal
from typing import Optional

from sqlmodel import Session, select

from alembic.main import engine
from models import Transaction
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

    def _get_cached_fee(self, address: str) -> Optional[Decimal]:
        with Session(engine) as session:
            stmt = select(Transaction).filter_by(tx_hash=address)
            transaction = session.exec(stmt).one_or_none()
            if transaction is None or transaction.eth_price is None:
                return None
            return (
                transaction.gas_used
                * transaction.gas_price
                / Decimal(10**18)
                * transaction.eth_price
            )

    def get_transaction_fee(self, address: str) -> Decimal:
        tx = self.transaction_client.get_single_transaction(address)
        eth_price = self.asset_price_client.get_price(tx.time_stamp)

        return tx.get_eth_used() * eth_price
