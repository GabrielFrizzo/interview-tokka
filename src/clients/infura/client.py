from hexbytes import HexBytes
from web3 import Web3

from clients.exceptions import ClientException
from config import Config
from models import Transaction
from services.transaction_client import TransactionClient


class InfuraClient(TransactionClient):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_single_transaction(self, tx_hash: str) -> Transaction:
        web3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{Config.INFURA_API_KEY}"))
        tx = web3.eth.get_transaction_receipt(HexBytes(tx_hash))
        block_number = tx.get("blockNumber")
        if block_number is None:
            raise ClientException(f"Transaction with hash {tx_hash} not found")
        timestamp = web3.eth.get_block(block_number).get("timestamp", 0)

        return Transaction(
            block_number=tx.get("blockNumber", 0),
            time_stamp=timestamp * 1000,
            tx_hash=str(tx.get("hash")),
            from_address=tx.get("from", ""),
            to_address=tx.get("to", ""),
            gas_price=tx.get("effectiveGasPrice", Web3.to_wei(0, "ether")),
            gas_used=tx.get("gasUsed", 0),
        )
