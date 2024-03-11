from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):
    tx_hash: str = Field(unique=True, primary_key=True)
    block_number: int
    time_stamp: Decimal = Field(max_digits=20, decimal_places=0)
    from_address: str
    to_address: str
    gas_price: Decimal = Field(max_digits=30, decimal_places=0)
    gas_used: Decimal = Field(max_digits=30, decimal_places=0)
    eth_price: Optional[Decimal] = Field(default=None)

    def get_eth_used(self) -> Decimal:
        return self.gas_used * self.gas_price / Decimal(10**18)

    def get_usdt_price(self) -> Decimal:
        if self.eth_price is None:
            raise ValueError("ETH price is not set")
        return self.eth_price * self.get_eth_used()
