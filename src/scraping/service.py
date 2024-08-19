import os, time
import requests

from pathlib import Path
from bs4 import BeautifulSoup

from src.scraping.schemas import ScrapeSettings, Product
from src.database import Database
from src.logging import logger
from src.config import BASE_URL, DATA_IMAGE_DIRETORY
from src.notification import Notification
from src.cache import Cache

class ScraperService:
    def __init__(self, settings: ScrapeSettings):
        self.settings = settings
        self.database = Database()
        self.notification = Notification()
        self.cache = Cache()

    def scrape(self):
        '''function that actually does the scraping and saves the results'''

        logger.info("Scraping started")
        message = 'fail'
        final_response = {}
        products = []
        page = 1
        try:
            while True:
                url = f"{BASE_URL}/page/{page}/"
                response = self._get_page(url)
                if response is None:
                    break
                soup = BeautifulSoup(response.content, "html.parser")
                product_elements = soup.find_all('li', class_='product')
                logger.info(f"Page number {page} - {len(product_elements)} products found!")
                for element in product_elements:
                    title = element.find('h2', class_='woo-loop-product__title').find('a')['href'].split('/')[-2]
                    price = element.find('span', class_='woocommerce-Price-amount').text.strip()
                    image_url = element.find('img', class_='attachment-woocommerce_thumbnail')['src']
                    if '.jpg' not in image_url:
                        image_url = element.find('img', class_='attachment-woocommerce_thumbnail')['data-lazy-src']
                    products.append(Product(
                        product_title=title,
                        product_price=price,
                        path_to_image=self._download_image(image_url)
                    ))
                if self.settings.limit_pages and page >= self.settings.limit_pages:
                    break
                page += 1
            logger.info(f'total products: {len(products)}')
            new_or_updated_products = []
            for product in products:
                logger.info(f'product name : {product.product_title}')
                if not self.cache.is_price_changed(product):
                    continue
                self.database.save(product)
                self.cache.update_cache(product)
                new_or_updated_products.append(product)
            self.notification.notify(f"{len(products)} products were scraped. {len(new_or_updated_products)} were upserted in DB")
            message = 'success'
            final_response = {
                "total_products_scraped" : len(products)
            }
        except Exception as e:
            logger.error(e)
            pass
        finally:
            return message, final_response

    def _get_page(self, url):
        '''this function returns the data on a single page of the url'''

        retries = 3
        for _ in range(retries):
            try:
                response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"} , proxies={"http": self.settings.proxy, "https": self.settings.proxy} if self.settings.proxy else None)
                if response.status_code == 200:
                    return response
            except requests.RequestException:
                time.sleep(5)
        return None

    def _download_image(self, url):
        '''this function saves the image data'''
        
        os.makedirs(DATA_IMAGE_DIRETORY, exist_ok=True)
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            path = f"{DATA_IMAGE_DIRETORY}/{os.path.basename(url)}"
            with open(path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return path
        return ""
