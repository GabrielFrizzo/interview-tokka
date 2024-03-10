from fastapi import FastAPI

from src.api.router import router

app = FastAPI(
    title="Tokka API",
    description="Backend for checking USDT equivalent of transaction fees on Uniswap V3's USDC/WETH pool",
)

app.include_router(router, prefix="/api")
