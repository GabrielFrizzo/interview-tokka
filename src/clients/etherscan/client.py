from typing import Iterator

import requests
from hexbytes import HexBytes
from web3 import Web3

from services.transaction_client import SwapTransactionClient
from src.config import Config

from .value_objects import EtherscanTransaction


class EtherscanClientException(Exception):
    pass


class EtherscanClient(SwapTransactionClient):
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.url = "https://api.etherscan.io/api"

    def get_swap_transactions(
        self, swap_contract_address, sort="desc"
    ) -> Iterator[EtherscanTransaction]:
        current_page = 1
        while True:
            print("starting next page", current_page)
            page = self.get_swap_transaction_page(swap_contract_address, current_page, sort)
            if not page:
                break
            yield from page
            current_page += 1

    def get_swap_transaction_page(
        self, swap_contract_address, page=1, sort="desc", page_size=100
    ) -> list[EtherscanTransaction]:
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

        return [EtherscanTransaction.from_json(item) for item in response_json["result"]]

    def get_single_transaction(self, tx_hash: str) -> EtherscanTransaction:
        web3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{Config.INFURA_API_KEY}"))
        tx = web3.eth.get_transaction_receipt(HexBytes(tx_hash))
        block_number = tx.get("blockNumber")
        if block_number is None:
            raise EtherscanClientException(f"Transaction with hash {tx_hash} not found")
        timestamp = web3.eth.get_block(block_number).get("timestamp", 0)

        return EtherscanTransaction(
            block_number=tx.get("blockNumber", 0),
            time_stamp=timestamp * 1000,
            hash=str(tx.get("hash")),
            nonce=tx.get("nonce", ""),
            block_hash=str(tx.get("blockHash")),
            transaction_index=tx.get("transactionIndex", 0),
            from_address=tx.get("from", ""),
            to_address=tx.get("to", ""),
            value=tx.get("value", ""),
            gas=tx.get("maxFeePerGas", 0),
            gas_price=tx.get("effectiveGasPrice", ""),
            contract_address=str(tx.get("contractAddress")),
            cumulative_gas_used=tx.get("cumulativeGasUsed", ""),
            gas_used=tx.get("gasUsed", 0),
            confirmations=tx.get("confirmations", ""),
        )
