import requests

from etherscan.value_objects import EtherscanTransaction


class EtherscanClientException(Exception):
    pass


class EtherscanClient:
    def __init__(self, api_key) -> None:
        self.api_key = api_key

    def get_token_transactions(
        self, address, page=1, sort="desc", page_size=100
    ) -> list[EtherscanTransaction]:
        url = "https://api.etherscan.io/api"
        params = {
            "module": "account",
            "action": "tokentx",
            "address": address,
            "apikey": self.api_key,
            "page": str(page),
            "sort": sort,
            "offset": str(page_size),
        }

        response = requests.request("GET", url, params=params)
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
