from decimal import Decimal

from fastapi import APIRouter

from clients.binance.binance_client import BinanceClient
from clients.infura.client import InfuraClient
from config import Config
from services.transaction_fee_service import TransactionFeeService

router = APIRouter()


@router.get("/{transaction_hash}/fee")
def get_transaction_fee(transaction_hash: str) -> Decimal:
    binance_client = BinanceClient("ETHUSDT")
    assert Config.INFURA_API_KEY is not None
    infura_client = InfuraClient(api_key=Config.INFURA_API_KEY)

    usd_fee = TransactionFeeService(
        asset_price_client=binance_client, transaction_client=infura_client
    ).get_transaction_fee(transaction_hash)

    return usd_fee


@router.get("/batch")
def get_batch_transaction_fee():
    pass
