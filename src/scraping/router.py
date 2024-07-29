from fastapi import APIRouter, Depends, HTTPException
from src.scraping.schemas import ScrapeSettings
from src.scraping.service import ScraperService
from src.scraping.dependencies import get_token_header

router = APIRouter()

@router.post("/", dependencies=[Depends(get_token_header)])
async def scrape(settings: ScrapeSettings):
    scraper_service = ScraperService(settings)
    products_scraped = scraper_service.scrape()
    return {"status": "success", "products_scraped": len(products_scraped)}
