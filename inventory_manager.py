import json

class InventoryManager:
    def __init__(self, inventory_file, products):
        self.inventory_file = inventory_file
        self.products = products
        self.load_inventory()

    def load_inventory(self):
        try:
            with open(self.inventory_file) as file:
                self.inventory = json.load(file)
        except FileNotFoundError:
            self.inventory = {}

    def save_inventory(self):
        with open(self.inventory_file, 'w') as file:
            json.dump(self.inventory, file, indent=4)

    def update_inventory(self, items):
        for item in items:
            for component, count in self.products[item]['components'].items():
                self.inventory[component] -= count
        self.save_inventory()

    def check_availability(self, item):
        if item in self.products:
            return all(self.inventory.get(component, 0) >= count for component, count in
                       self.products[item]['components'].items())
        return False
