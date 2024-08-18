import os, time
import requests

from pathlib import Path
from bs4 import BeautifulSoup

from src.scraping.schemas import ScrapeSettings, Product
from src.database import Database
from src.config import DATA_DIRECTORY, DATA_IMAGE_DIRETORY
from src.notification import Notification
from src.cache import Cache

class ScraperService:
    def __init__(self, settings: ScrapeSettings):
        self.base_url = "https://dentalstall.com/shop/"
        self.settings = settings
        self.database = Database()
        self.notification = Notification()
        self.cache = Cache()

    def scrape(self):
        print('starting scraping!')
        products = []
        page = 1
        while True:
            url = f"{self.base_url}/page/{page}/"
            response = self._get_page(url)
            if response is None:
                break

            soup = BeautifulSoup(response.content, "html.parser")
            product_elements = soup.find_all('li', class_='product')
            print(f"Page number {page} - {len(product_elements)} products found!")
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
        print('total :', len(products))
        new_products = []
        for product in products:
            print('product name :', product.product_title)
            if not self.cache.is_price_changed(product):
                continue
            self.database.save(product)
            self.cache.update_cache(product)
            new_products.append(product)

        self.notification.notify(f"{len(new_products)} products scraped and updated in DB during the current session.")
        return new_products

    def _get_page(self, url):
        retries = 3
        for _ in range(retries):
            try:
                response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"} , proxies={"http": self.settings.proxy, "https": self.settings.proxy} if self.settings.proxy or self.settings.proxy != "string" else None)
                if response.status_code == 200:
                    return response
            except requests.RequestException:
                time.sleep(5)
        return None

    def _download_image(self, url):
        os.makedirs(DATA_IMAGE_DIRETORY, exist_ok=True)
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            path = f"{DATA_IMAGE_DIRETORY}/{os.path.basename(url)}"
            with open(path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return path
        return ""
