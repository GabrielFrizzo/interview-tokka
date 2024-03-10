from typing import Iterator

import requests
from hexbytes import HexBytes
from web3 import Web3

from config import Config
from core.value_objects import Transaction
from services.transaction_client import SwapTransactionClient


class EtherscanClientException(Exception):
    pass


class EtherscanClient(SwapTransactionClient):
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.url = "https://api.etherscan.io/api"

    def get_swap_transactions(self, swap_contract_address, sort="desc") -> Iterator[Transaction]:
        current_page = 1
        while True:
            page = self.get_swap_transaction_page(swap_contract_address, current_page, sort)
            if not page:
                break
            yield from page
            current_page += 1

    def get_swap_transaction_page(
        self, swap_contract_address, page=1, sort="desc", page_size=100
    ) -> list[Transaction]:
        params = {
            "module": "account",
            "action": "tokentx",
            "address": swap_contract_address,
            "apikey": self.api_key,
            "page": str(page),
            "sort": sort,
            "offset": str(page_size),
        }

        response = requests.request("GET", self.url, params=params)
        if response.status_code != 200:
            raise EtherscanClientException(
                f"Request failed with status code {response.status_code}, response: {response.text}"
            )

        response_json = response.json()
        if response_json["status"] != "1":
            raise EtherscanClientException(
                f"Request failed with status code {response_json['status']}, response: {response_json['message']}"
            )

        return [Transaction.from_json(item) for item in response_json["result"]]

    def get_single_transaction(self, tx_hash: str) -> Transaction:
        web3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{Config.INFURA_API_KEY}"))
        tx = web3.eth.get_transaction_receipt(HexBytes(tx_hash))
        block_number = tx.get("blockNumber")
        if block_number is None:
            raise EtherscanClientException(f"Transaction with hash {tx_hash} not found")
        timestamp = web3.eth.get_block(block_number).get("timestamp", 0)

        return Transaction(
            block_number=tx.get("blockNumber", 0),
            time_stamp=timestamp * 1000,
            hash=str(tx.get("hash")),
            from_address=tx.get("from", ""),
            to_address=tx.get("to", ""),
            gas_price=tx.get("effectiveGasPrice", Web3.to_wei(0, "ether")),
            gas_used=tx.get("gasUsed", 0),
        )
