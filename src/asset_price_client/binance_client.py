from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from binance.spot import Spot  # type: ignore

from asset_price_client.asset_price_client import AssetPriceClient


@dataclass
class KlineResponse:
    open_time: int
    open: str
    high: str
    low: str
    close: str
    volume: str
    close_time: int
    quote_asset_volume: str
    number_of_trades: int
    taker_buy_base_asset_volume: str
    taker_buy_quote_asset_volume: str
    ignore: str

    @staticmethod
    def from_api(result: list) -> "KlineResponse":
        return KlineResponse(
            open_time=result[0],
            open=result[1],
            high=result[2],
            low=result[3],
            close=result[4],
            volume=result[5],
            close_time=result[6],
            quote_asset_volume=result[7],
            number_of_trades=result[8],
            taker_buy_base_asset_volume=result[9],
            taker_buy_quote_asset_volume=result[10],
            ignore=result[11],
        )


class BinanceClient(AssetPriceClient):
    def __init__(self, symbol: str) -> None:
        self.client = Spot()
        super().__init__(symbol)

    def get_price(self, dt: datetime) -> Decimal:
        response = self.client.klines(
            symbol=self.symbol,
            interval="1m",
            limit=1,
            startTime=int(dt.timestamp() * 1000) - 60000,
            endTime=int(dt.timestamp() * 1000),
        )
        kline = KlineResponse.from_api(response[0])
        return Decimal(kline.close)
