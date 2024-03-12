from decimal import Decimal

from alembic.main import engine
from background.tasks import process_batch_imports
from clients.binance.binance_client import BinanceClient
from clients.infura.client import InfuraClient
from config import Config
from fastapi import APIRouter
from models import BlockWindow, ImportingJob
from services.transaction_fee_service import TransactionFeeService
from sqlmodel import Session

router = APIRouter()


@router.get("/{transaction_hash}/fee")
def get_transaction_fee(transaction_hash: str) -> Decimal:
    binance_client = BinanceClient("ETHUSDT")
    assert Config.INFURA_API_KEY is not None
    infura_client = InfuraClient(api_key=Config.INFURA_API_KEY)

    with Session(engine) as session:
        usd_fee = TransactionFeeService(
            asset_price_client=binance_client,
            transaction_client=infura_client,
            session=session,
        ).get_transaction_fee(transaction_hash)

        session.commit()

    return usd_fee


@router.get("/batch")
def get_batch_transaction_fee(block_window: BlockWindow):
    with Session(engine) as session:
        job = ImportingJob(start_block_number=block_window.start, end_block_number=block_window.end)
        session.add(job)
        session.commit()
    process_batch_imports.delay(str(job.id))
