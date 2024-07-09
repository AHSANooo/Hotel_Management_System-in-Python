import json

class ProductManager:
    def __init__(self, products_file):
        self.products_file = products_file
        self.load_products()

    def load_products(self):
        try:
            with open(self.products_file) as file:
                self.products = json.load(file)
        except FileNotFoundError:
            self.products = {}
