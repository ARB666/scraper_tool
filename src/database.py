import json
from src.scraping.schemas import Product

class Database:
    def __init__(self, filename="data/products.json"):
        self.filename = filename

    def save(self, product: Product):
        print('saving product in db')
        products = self._load_products()
        product_json = product.model_dump()
        for i,p in enumerate(products):
            if p['product_title'] == product_json['product_title']:
                products.pop(i)
        products.append(product.model_dump())
        self._save_products(products)

    def _load_products(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _save_products(self, products):
        with open(self.filename, "w") as file:
            json.dump(products, file, indent=4)
