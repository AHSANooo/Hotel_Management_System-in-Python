""""
import json
import re
from datetime import datetime
from collections import Counter


class InventoryManager:
    def __init__(self, inventory_file, products):
        self.inventory_file = inventory_file
        self.products = products
        self.load_inventory()

    def load_inventory(self):
        try:
           self.inventory = json.load(open(self.inventory_file))
        except FileNotFoundError:
            self.inventory = {}

    def save_inventory(self):
        json.dump(self.inventory, open(self.inventory_file, 'w'), indent=4)

    def update_inventory(self, items):
        for item in items:
            components = self.products[item]['components']
            for component, count in components.items():
                self.inventory[component] -= count
        self.save_inventory()

    def check_availability(self, item):
        if item in self.products:
            return all(self.inventory.get(component, 0) >= count for component, count in
                       self.products[item]['components'].items())
        return False


class OrderManager:
    def __init__(self, orders_file):
        self.orders_file = orders_file
        self.load_orders()

    def load_orders(self):
        try:
            self.orders = json.load(open(self.orders_file))
        except FileNotFoundError:
            self.orders = []

    def save_orders(self):
        json.dump(self.orders, open(self.orders_file, 'w'), indent=4)

    def place_order(self, customer_name, items, payment_method, total, total_discount, total_after_discount):
        order = {
            'customer_name': customer_name,
            'items': items,
            'payment_method': payment_method,
            'total': total,
            'total_discount': total_discount,
            'total_after_discount': total_after_discount,
            'datetime': datetime.now().isoformat()
        }
        self.orders.append(order)
        self.save_orders()
        return order


class KFCManagementSystem:
    def __init__(self):
        self.order_manager = OrderManager('orders.json')
        self.products_file = 'products.json'
        self.load_products()

    def load_products(self):
        try:
            self.products = json.load(open(self.products_file))
        except FileNotFoundError:
            self.products = {}

        self.inventory_manager = InventoryManager('inventory.json', self.products)

    def welcome_screen(self):
        print("Welcome to KFC!\n")
        self.customer_name = input("Please enter your full name: ").strip().upper()
        if not re.match("^[A-Za-z ]+$", self.customer_name):
            print("\nInvalid input. Please enter a valid name.")
            return self.welcome_screen()

        self.select_items()

    def get_available_items(self):
        return {item: details for item, details in self.products.items() if self.inventory_manager.check_availability(item)}

    def select_items(self):
        selected_items = []
        available_items = self.get_available_items()

        while True:
            if not available_items:
                print("\nSorry, no items are available at the moment.")
                return

            print("\nAvailable items:")
            item_map = self.display_available_items(available_items)

            choice = input("\nEnter your choice (number): ").strip()
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(item_map) + 1:
                print("\nInvalid choice. Please enter a valid number.")
                continue

            if int(choice) == len(item_map) + 1:
                break

            selected_item = item_map[int(choice)]
            max_qty = self.get_max_quantity(selected_item)
            qty = input(f"Enter quantity for {selected_item} (Max: {max_qty}): ").strip()
            if not qty.isdigit() or int(qty) < 1 or int(qty) > max_qty:
                print(f"\nInvalid quantity. Please enter a number between 1 and {max_qty}.")
                continue

            qty = int(qty)
            selected_items.extend([selected_item] * qty)

        if not selected_items:
            print("\nNo items selected. Please select at least one item.")
            return self.select_items()

        self.payment_method(selected_items)

    def display_available_items(self, available_items):
        item_map = {}
        for index, (item, details) in enumerate(available_items.items(), start=1):
            price_info = f"Rs.{details['price']}"
            if 'discount' in details:
                price_info += f" (Discount: {details['discount']}%)"
            print(f"{index}. {item}: {price_info}")
            item_map[index] = item
        print(f"{index + 1}. Done")
        return item_map

    def get_max_quantity(self, selected_item):
        components = self.products[selected_item]['components']
        return min(self.inventory_manager.inventory[component] // count for component, count in components.items())

    def payment_method(self, selected_items):
        print("\nSelect Payment Method:")
        print("1. Card")
        print("2. Cash")

        choice = input("\nEnter your choice (number): ").strip()

        if choice == '1':
            payment_method = 'card'
        elif choice == '2':
            payment_method = 'cash'
        else:
            print("\nInvalid choice. Please enter '1' or '2'.")
            return self.payment_method(selected_items)

        self.apply_discounts(selected_items, payment_method)

    def get_order_count(self):
        return sum(1 for order in self.order_manager.orders if order['customer_name'] == self.customer_name)

    def apply_discounts(self, selected_items, payment_method):
        total = sum(self.products[item]['price'] for item in selected_items)
        discount = self.calculate_discount(payment_method, selected_items)
        total_after_discount = total * (1 - discount)
        self.store_order(selected_items, payment_method, total_after_discount, discount, total)

    def calculate_discount(self, payment_method, selected_items):
        discount = 0.05 if payment_method == 'card' else 0
        order_count = self.get_order_count()
        if order_count > 0:
            discount += 0.027
            if order_count > 10:
                discount += 0.12
        for item in selected_items:
            if 'discount' in self.products[item]:
                discount += self.products[item]['discount'] / 100
        return discount

    def store_order(self, selected_items, payment_method, total_after_discount, total_discount, total):
        self.order_manager.place_order(self.customer_name, selected_items, payment_method, total, total_discount, total_after_discount)
        self.print_receipt(selected_items, payment_method, total_after_discount, total_discount, total)
        self.inventory_manager.update_inventory(selected_items)

    def print_receipt(self, selected_items, payment_method, total_after_discount, total_discount, total):
        item_summary = Counter(selected_items)
        item_summary_str = ', '.join(f"{item} x {count}" for item, count in item_summary.items())
        print("Order placed successfully!")
        print(f"Customer Name: {self.customer_name}")
        print(f"Items: {item_summary_str}")
        print(f"Payment Method: {payment_method}")
        print(f"Bill: Rs.{total}/-")
        print(f"Discount: {total_discount * 100}%")
        print(f"Total Amount to be Paid: Rs.{total_after_discount:.2f}/-")
        print(f"Date and Time: {datetime.now().date()} {datetime.now().strftime('%H:%M')}")


if __name__ == "__main__":
    system = KFCManagementSystem()
    system.welcome_screen()
"""


from kfc_management_system import KFCManagementSystem

if __name__ == "__main__":
    system = KFCManagementSystem()
    system.welcome_screen()
