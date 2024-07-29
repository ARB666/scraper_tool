import redis
from src.config import REDIS_HOST, REDIS_PORT
from src.scraping.schemas import Product

class Cache:
    def __init__(self):
        self.client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    def is_price_changed(self, product: Product):
        cached_price = self.client.get(product.product_title)
        cached_price = cached_price.decode('utf-8') if cached_price else None
        print('cached_price :', cached_price)
        print('actual price', product.product_price)
        return cached_price is None or cached_price != product.product_price

    def update_cache(self, product: Product):
        print('saving product in cache')
        self.client.set(product.product_title, product.product_price)
