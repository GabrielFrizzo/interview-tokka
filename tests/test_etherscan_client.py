from pprint import pprint

from etherscan.client import EtherscanClient


def test_get_token_transactions() -> None:
    client = EtherscanClient("IHF6CDIVFN731EBFCFKFTZE3XYRKUKHXSN")
    response = client.get_token_transactions(
        "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640", page_size=10
    )
    pprint(response)
