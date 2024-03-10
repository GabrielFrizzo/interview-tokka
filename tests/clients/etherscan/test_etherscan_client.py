from clients.etherscan.client import EtherscanClient
from config import Config


def test_get_swap_transactions() -> None:
    client = EtherscanClient(Config.ETHERSCAN_API_KEY)
    response = client.get_swap_transactions("0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640")
    for i in range(10):
        assert next(response)
