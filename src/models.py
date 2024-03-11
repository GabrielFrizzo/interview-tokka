from decimal import Decimal

from sqlmodel import Field, SQLModel


class TransactionBase(SQLModel, table=True):
    tx_hash: str = Field(unique=True, primary_key=True)
    block_number: int
    time_stamp: int
    from_address: str
    to_address: str
    gas_price: int
    gas_used: int
    eth_price: Decimal
