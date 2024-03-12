import os


class Config:
    ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
    INFURA_API_KEY = os.getenv("INFURA_API_KEY")
    START_BLOCK_NUMBER = int(
        os.getenv("START_BLOCK_NUMBER", 12_300_000)
    )  # First block of the contract
