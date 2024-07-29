from fastapi import FastAPI
from src.scraping.router import router as scraping_router

app = FastAPI()

app.include_router(scraping_router, prefix="/scrape", tags=["scrape"])
