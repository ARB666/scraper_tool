from fastapi import APIRouter, Depends, HTTPException
from src.scraping.schemas import ScrapeSettings, ResponseModel
from src.scraping.service import ScraperService
from src.scraping.dependencies import get_token_header

router = APIRouter()

@router.post("/", dependencies=[Depends(get_token_header)], response_model=ResponseModel)
async def scrape(settings: ScrapeSettings):
    scraper_service = ScraperService(settings)
    message, response = scraper_service.scrape()
    if message == 'success':
        return ResponseModel(message = message, response = response)
    elif message == 'fail':
        HTTPException(status_code=500, detail="Internal Error")