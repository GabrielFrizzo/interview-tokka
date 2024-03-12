from datetime import datetime, timedelta

from alembic.main import engine
from clients.binance.binance_client import BinanceClient
from clients.etherscan.client import EtherscanClient
from clients.infura.client import InfuraClient
from config import Config
from models import ImportingJob, JobStatus
from services.batch_fee_service import BatchFeeService
from services.transaction_fee_service import TransactionFeeService
from sqlalchemy import text
from sqlmodel import Session, and_, select

from background.main import celery_app


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task()
def periodical_batch_job_creation():
    with Session(engine) as session:
        stmt = """
            SELECT new_start, new_end AS new_end
            FROM (SELECT (start.end_block_number + 1) AS new_start, (end_.start_block_number - 1) AS new_end
                    FROM importingjob start, importingjob end_
                    WHERE end_.start_block_number > start.end_block_number + 1 AND
                    NOT EXISTS (SELECT * FROM importingjob AS mid
                                WHERE mid.start_block_number > start.end_block_number
                                AND mid.end_block_number < end_.start_block_number
                                )
                UNION
                SELECT MAX(end_.end_block_number + 1) AS new_start, NULL AS new_end
                    FROM importingjob AS end_
                ) derived
            ORDER BY new_start LIMIT 1;"""
        result = session.execute(text(stmt)).first()
        if result is None:
            return
        new_start, new_end = result
        if new_start is None:
            new_start = 0
        if new_end is None:
            new_end = new_start + 9999

        for start in range(new_start, new_end, 1000):
            session.add(
                ImportingJob(start_block_number=start, end_block_number=min(new_end, start + 999))
            )
        session.commit()


@celery_app.task()
def periodical_process_batch_imports() -> None:
    with Session(engine) as session:
        stmt = select(ImportingJob).filter_by(status=JobStatus.FAILED)
        failed_importing_job = session.exec(stmt).first()
        if failed_importing_job is not None:
            process_batch_imports.delay(str(failed_importing_job.id))
            return

        stmt = select(ImportingJob).where(
            and_(
                ImportingJob.status == JobStatus.IN_PROGRESS,
                ImportingJob.created_at < datetime.now() - timedelta(hours=1),
                # If the job has been running for more than an hour, we assume it has failed
            )
        )
        timed_out_importing_job = session.exec(stmt).first()
        if timed_out_importing_job is not None:
            process_batch_imports.delay(str(timed_out_importing_job.id))
            return

        stmt = select(ImportingJob).filter_by(status=JobStatus.PENDING)
        pending_importing_job = session.exec(stmt).first()
        if pending_importing_job is not None:
            process_batch_imports.delay(str(pending_importing_job.id))
            return


@celery_app.task()
def process_batch_imports(job_id: str) -> list[str]:
    binance_client = BinanceClient("ETHUSDT")
    assert Config.INFURA_API_KEY is not None
    infura_client = InfuraClient(api_key=Config.INFURA_API_KEY)
    assert Config.ETHERSCAN_API_KEY is not None
    etherscan_client = EtherscanClient(api_key=Config.ETHERSCAN_API_KEY)

    with Session(engine) as session:
        job = session.exec(select(ImportingJob).filter_by(id=job_id)).one()
        job.status = JobStatus.IN_PROGRESS
        session.commit()
        transaction_fee_service = TransactionFeeService(
            asset_price_client=binance_client,
            transaction_client=infura_client,
            session=session,
        )
        try:
            transactions = BatchFeeService(
                swap_transaction_client=etherscan_client,
                transaction_fee_service=transaction_fee_service,
            ).get_batch_transactions(job)
        except Exception as e:
            job.status = JobStatus.FAILED
            session.commit()
            raise e

        job.status = JobStatus.COMPLETED
        session.commit()

    periodical_process_batch_imports.delay()
    return [transaction.tx_hash for transaction in transactions]
