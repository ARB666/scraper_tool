from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    product_title: str
    product_price: str
    path_to_image: str

class ScrapeSettings(BaseModel):
    limit_pages: Optional[int] = 100
    proxy: Optional[str] = None