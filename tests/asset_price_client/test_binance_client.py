from datetime import datetime

from asset_price_client.binance_client import BinanceClient


def test_get_price() -> None:
    client = BinanceClient("ETHUSDT")
    response = client.get_price(datetime.now())
    print(response)
    assert response > 0
