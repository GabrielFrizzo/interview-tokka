from clients.etherscan.client import EtherscanClient
from config import Config
from models import BlockWindow


def test_get_swap_transactions() -> None:
    client = EtherscanClient(Config.ETHERSCAN_API_KEY)
    response = client.get_swap_transactions(
        "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
        BlockWindow(start=0, end=1_000_000_000),
    )
    for _ in range(10):
        assert next(response)
