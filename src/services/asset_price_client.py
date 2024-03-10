from abc import ABC, abstractmethod
from decimal import Decimal


class AssetPriceClient(ABC):
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    @abstractmethod
    def get_price(self, timestamp: int) -> Decimal:
        pass
