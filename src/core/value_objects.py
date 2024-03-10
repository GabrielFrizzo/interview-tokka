from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Transaction:
    block_number: int
    time_stamp: int
    hash: str
    from_address: str
    to_address: str
    gas_price: int
    gas_used: int

    def get_eth_used(self) -> Decimal:
        return Decimal(self.gas_used) * Decimal(self.gas_price) / Decimal(10**18)

    @staticmethod
    def from_json(json) -> "Transaction":
        return Transaction(
            block_number=int(json["blockNumber"]),
            time_stamp=int(json["timeStamp"]),
            hash=json["hash"],
            from_address=json["from"],
            to_address=json["to"],
            gas_price=int(json["gasPrice"]),
            gas_used=int(json["gasUsed"]),
        )
