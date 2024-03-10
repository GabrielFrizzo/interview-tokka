from pprint import pprint

import pytest

from etherscan.client import EtherscanClient, EtherscanClientException


def test_get_token_transactions() -> None:
    client = EtherscanClient("IHF6CDIVFN731EBFCFKFTZE3XYRKUKHXSN")
    response = client.get_token_transactions(
        "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640", page_size=10
    )
    assert len(response) == 10
    pprint(response)


def test_error_on_request() -> None:
    client = EtherscanClient("IHF6CDIVFN731EBFCFKFTZE3XYRKUKHXSN")
    with pytest.raises(EtherscanClientException):
        client.get_token_transactions("0x88e6a0c2ddd26feeb64f039a2c410")
