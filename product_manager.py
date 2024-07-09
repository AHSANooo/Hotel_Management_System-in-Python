import json

class ProductManager:
    def __init__(self, products_file):
        self.products_file = products_file
        self.load_products()

    def load_products(self):
        try:
            self.products = json.load(open(self.products_file))
        except FileNotFoundError:
            self.products = {}
