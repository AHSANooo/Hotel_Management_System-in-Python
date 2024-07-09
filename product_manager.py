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

    def save_products(self):
        json.dump(self.products, open(self.products_file, 'w'), indent=4)

    def add_product(self, product_id, product_details):
        self.products[product_id] = product_details
        self.save_products()

    def remove_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            self.save_products()
        else:
            print(f"Product with ID '{product_id}' not found.")

    def update_product(self, product_id, new_details):
        if product_id in self.products:
            self.products[product_id].update(new_details)
            self.save_products()
        else:
            print(f"Product with ID '{product_id}' not found.")

    def get_product(self, product_id):
        return self.products.get(product_id, None)

    def get_all_products(self):
        return self.products.copy()

    def filter_products(self, criteria):
        filtered_products = {}
        for product_id, details in self.products.items():
            if all(criteria.get(key, details[key]) == details[key] for key in criteria):
                filtered_products[product_id] = details
        return filtered_products

    def product_exists(self, product_id):
        return product_id in self.products