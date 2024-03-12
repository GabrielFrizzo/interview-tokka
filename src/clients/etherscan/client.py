from decimal import Decimal
from typing import Iterator

import requests
from models import BlockWindow, Transaction
from services.transaction_client import SwapTransactionClient

from clients.exceptions import ClientException


class EtherscanClient(SwapTransactionClient):
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.url = "https://api.etherscan.io/api"

    def get_swap_transactions(
        self, swap_contract_address: str, block_window: BlockWindow, sort="desc"
    ) -> Iterator[Transaction]:
        current_page = 1
        while True:
            page = self.get_swap_transaction_page(
                swap_contract_address, block_window, current_page, sort
            )
            if not page:
                break
            yield from page
            current_page += 1

    def get_swap_transaction_page(
        self,
        swap_contract_address: str,
        block_window: BlockWindow,
        page=1,
        sort="desc",
        page_size=1_000,
    ) -> list[Transaction]:
        params = {
            "module": "account",
            "action": "tokentx",
            "address": swap_contract_address,
            "apikey": self.api_key,
            "page": str(page),
            "startblock": str(block_window.start),
            "endblock": str(block_window.end),
            "sort": sort,
            "offset": str(page_size),
        }

        response = requests.request("GET", self.url, params=params)
        if response.status_code != 200:
            raise ClientException(
                f"Request failed with status code {response.status_code}, response: {response.text}"
            )

        response_json = response.json()
        if response_json["status"] != "1":
            if (
                response_json["message"] == "No transactions found"
            ):  # Etherscan treats this as an error, but we want just the empty list
                return []
            raise ClientException(
                f"Request failed with json status {response_json['status']}, response: {response_json['message']}"
            )

        return [self._make_transaction(item) for item in response_json["result"]]

    def _make_transaction(self, json: dict) -> Transaction:
        return Transaction(
            block_number=int(json["blockNumber"]),
            time_stamp=Decimal(json["timeStamp"]),
            tx_hash=json["hash"],
            from_address=json["from"],
            to_address=json["to"],
            gas_price=Decimal(json["gasPrice"]),
            gas_used=Decimal(json["gasUsed"]),
        )
