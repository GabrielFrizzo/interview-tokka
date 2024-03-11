from decimal import Decimal
from typing import Optional

from models import Transaction
from services.asset_price_client import AssetPriceClient
from services.transaction_client import TransactionClient
from sqlmodel import Session, select


class TransactionFeeService:
    def __init__(
        self,
        transaction_client: TransactionClient,
        asset_price_client: AssetPriceClient,
        session: Session,
    ) -> None:
        self.transaction_client = transaction_client
        self.asset_price_client = asset_price_client
        self.session = session

    def _get_cached_transaction(self, address: str) -> Optional[Transaction]:
        stmt = select(Transaction).filter_by(tx_hash=address)
        transaction = self.session.exec(stmt).one_or_none()
        return transaction

    def get_transaction_fee(self, address: str) -> Decimal:
        cached_tx = self._get_cached_transaction(address)
        if cached_tx:
            tx = cached_tx
        else:
            tx = self.transaction_client.get_single_transaction(address)
            self.session.add(tx)

        if tx.eth_price is None:
            tx.eth_price = self.asset_price_client.get_price(int(tx.time_stamp))
            self.session.add(tx)

        return tx.get_eth_used() * tx.eth_price
