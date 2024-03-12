from decimal import Decimal
from typing import Optional

from alembic.main import engine
from background.tasks import process_batch_imports
from clients.binance.binance_client import BinanceClient
from clients.infura.client import InfuraClient
from config import Config
from fastapi import APIRouter
from models import BlockWindow, ImportingJob, JobStatus, Transaction
from pydantic import BaseModel
from services.transaction_fee_service import TransactionFeeService
from sqlmodel import Session, select

router = APIRouter()


class TransactionFeeResponse(BaseModel):
    transaction: Transaction
    fee_in_usdt: Decimal


@router.get("/{transaction_hash}/fee")
def get_transaction_fee(transaction_hash: str) -> TransactionFeeResponse:
    binance_client = BinanceClient("ETHUSDT")
    assert Config.INFURA_API_KEY is not None
    infura_client = InfuraClient(api_key=Config.INFURA_API_KEY)

    with Session(engine) as session:
        transaction = TransactionFeeService(
            asset_price_client=binance_client,
            transaction_client=infura_client,
            session=session,
        ).get_transaction_with_fee(transaction_hash)

        session.commit()

        return TransactionFeeResponse(
            fee_in_usdt=transaction.get_usdt_price(), transaction=transaction
        )


class GetBatchApiResponse(BaseModel):
    job_id: str


@router.post("/batch")
def get_batch_transaction_fee(block_window: BlockWindow) -> GetBatchApiResponse:
    with Session(engine) as session:
        job = ImportingJob(start_block_number=block_window.start, end_block_number=block_window.end)
        session.add(job)
        session.commit()
        process_batch_imports.delay(str(job.id))
        return GetBatchApiResponse(job_id=str(job.id))


class PostBatchApiResponse(BaseModel):
    status: str
    transactions: Optional[list[TransactionFeeResponse]] = None


@router.get("/batch/{job_id}")
def get_job_status(job_id: str):
    with Session(engine) as session:
        job = session.get(ImportingJob, job_id)
        if job is None:
            raise ValueError("Job not found")

        if job.status == JobStatus.COMPLETED:
            transactions = session.exec(
                select(Transaction).where(
                    Transaction.block_number >= job.start_block_number,
                    Transaction.block_number <= job.end_block_number,
                )
            ).all()
            return PostBatchApiResponse(
                status=job.status.name,
                transactions=[
                    TransactionFeeResponse(
                        transaction=transaction,
                        fee_in_usdt=transaction.get_usdt_price(),
                    )
                    for transaction in transactions
                ],
            )
        return PostBatchApiResponse(status=job.status.name)
