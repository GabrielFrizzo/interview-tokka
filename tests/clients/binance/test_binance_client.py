from datetime import datetime

from clients.binance.binance_client import BinanceClient


def test_get_price() -> None:
    client = BinanceClient("ETHUSDT")
    response = client.get_price(int(datetime.now().timestamp() * 1000))
    print(response)
    assert response > 0
