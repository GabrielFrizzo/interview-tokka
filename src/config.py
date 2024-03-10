import os


class Config:
    ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
    INFURA_API_KEY = os.getenv("INFURA_API_KEY")
