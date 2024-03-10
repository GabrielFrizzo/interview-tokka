from dataclasses import dataclass


@dataclass
class EtherscanTransaction:
    block_number: int
    time_stamp: int
    hash: str
    nonce: int
    block_hash: str
    transaction_index: int
    from_address: str
    to_address: str
    value: int
    gas: int
    gas_price: int
    input: str
    contract_address: str
    cumulative_gas_used: int
    gas_used: int
    confirmations: int

    @staticmethod
    def from_json(json):
        return EtherscanTransaction(
            block_number=int(json['blockNumber']),
            time_stamp=int(json['timeStamp']),
            hash=json['hash'],
            nonce=int(json['nonce']),
            block_hash=json['blockHash'],
            transaction_index=int(json['transactionIndex']),
            from_address=json['from'],
            to_address=json['to'],
            value=int(json['value']),
            gas=int(json['gas']),
            gas_price=int(json['gasPrice']),
            input=json['input'],
            contract_address=json['contractAddress'],
            cumulative_gas_used=int(json['cumulativeGasUsed']),
            gas_used=int(json['gasUsed']),
            confirmations=int(json['confirmations']),
        )