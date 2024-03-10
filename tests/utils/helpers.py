import random
from datetime import datetime, timedelta

from core.value_objects import Transaction


def get_random_transaction(
    block_number=None,
    time_stamp=None,
    hash=None,
    from_address=None,
    to_address=None,
    gas_price=None,
    gas_used=None,
) -> Transaction:
    return Transaction(
        block_number=block_number or random.randint(1, 1000),
        time_stamp=time_stamp
        or int((datetime.now() - timedelta(days=random.randint(1, 600))).timestamp() * 1000),
        hash=hash or "0x",
        from_address=from_address or "0x",
        to_address=to_address or "0x",
        gas_price=gas_price or 123,
        gas_used=gas_used or 123,
    )
