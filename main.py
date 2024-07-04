
import json
import re
from datetime import datetime
from collections import Counter


class KFCManagementSystem:

    def __init__(self):
        self.inventory_file = 'inventory.json'
        self.orders_file = 'orders.json'
        self.products_file = 'products.json'
        self.load_inventory()
        self.load_orders()
        self.load_products()

    def load_inventory(self):
        try:
            with open(self.inventory_file, 'r') as file:
                self.inventory = json.load(file)
        except FileNotFoundError:
            self.inventory = {}

    def save_inventory(self):
        with open(self.inventory_file, 'w') as file:
            json.dump(self.inventory, file, indent=4)

    def load_orders(self):
        try:
            with open(self.orders_file, 'r') as file:
                self.orders = json.load(file)
        except FileNotFoundError:
            self.orders = []

    def save_orders(self):
        with open(self.orders_file, 'w') as file:
            json.dump(self.orders, file, indent=4)

    def load_products(self):
        try:
            with open(self.products_file, 'r') as file:
                self.products = json.load(file)
        except FileNotFoundError:
            self.products = {}

    def welcome_screen(self):
        print("Welcome to KFC!\n\n")
        self.customer_name = input("Please enter your full name: ").strip().upper()
        if not re.match("^[A-Za-z ]+$", self.customer_name):
            print("\nInvalid input. Please enter a valid name.")
            return self.welcome_screen()
        self.select_items()

    def get_available_items(self):
        available_items = {}
        for item, details in self.products.items():
            if all(self.inventory.get(component, 0) >= count for component, count in details['components'].items()):
                available_items[item] = details
        return available_items

    def select_items(self):
        selected_items = []
        available_items = self.get_available_items()

        while True:
            if not available_items:
                print("\nSorry, no items are available at the moment.")
                return

            print("\nAvailable items:")
            index = 1
            item_map = {}
            for item, details in available_items.items():
                max_qty = min(self.inventory[component] // count for component, count in details['components'].items())
                print(f"{index}. {item}: Rs.{details['price']} (Max: {max_qty})")
                item_map[index] = item
                index += 1

            print(f"{index}. Done")
            choice = input("\nEnter your choice (number): ").strip()
            if not choice.isdigit() or int(choice) < 1 or int(choice) > index:
                print("\nInvalid choice. Please enter a valid number.")
                continue

            if choice == str(index):
                break

            selected_item = item_map[int(choice)]
            max_qty = min(self.inventory[component] // count for component, count in self.products[selected_item]['components'].items())
            qty = input(f"Enter quantity for {selected_item} (Max: {max_qty}): ").strip()
            if not qty.isdigit() or int(qty) < 1 or int(qty) > max_qty:
                print(f"\nInvalid quantity. Please enter a number between 1 and {max_qty}.")
                continue

            qty = int(qty)
            selected_items.extend([selected_item] * qty)

            for component, count in self.products[selected_item]['components'].items():
                self.inventory[component] -= count * qty

        if not selected_items:
            print("\nNo items selected. Please select at least one item.")
            return self.select_items()
        self.payment_method(selected_items)

    def payment_method(self, selected_items):
        payment_method = input("\nEnter payment method (Card/Cash): ").strip().lower()
        if payment_method not in ['card', 'cash']:
            print("\nInvalid payment method. Please enter 'Card' or 'Cash'.")
            return self.payment_method(selected_items)
        self.apply_discounts(selected_items, payment_method)

    def get_order_count(self):
        return sum(1 for order in self.orders if order['customer_name'] == self.customer_name)

    def apply_discounts(self, selected_items, payment_method):
        total = sum(self.products[item]['price'] for item in selected_items)
        discount = 0
        if payment_method == 'card':
            discount += 0.05
        order_count = self.get_order_count()
        if order_count > 0:
            discount += 0.027
            if order_count > 10:
                discount += 0.12
        total_after_discount = total * (1 - discount)
        self.store_order(selected_items, payment_method, total_after_discount, discount, total)

    def store_order(self, selected_items, payment_method, total_after_discount, total_discount, total):
        order = {
            'customer_name': self.customer_name,
            'items': selected_items,
            'payment_method': payment_method,
            'total': total_after_discount,
            'datetime': datetime.now().isoformat()
        }
        self.orders.append(order)
        self.save_orders()
        item_summary = Counter(selected_items)
        item_summary_str = ', '.join(f"{item} x {count}" for item, count in item_summary.items())
        print("Order placed successfully!")
        print(f"Customer_name : {self.customer_name}")
        print(f"Items : {item_summary_str}")
        print(f"Payment Method :  {payment_method}")
        print(f"Bill : Rs.{total}/-")
        print(f"Discount : {total_discount*100}%")
        print(f"Total amount to be paid: Rs.{total_after_discount:.2f}/.")
        print(f"Date and time : {datetime.now().date()}   {datetime.now().strftime('%H:%M')}")

        self.update_inventory(selected_items)

    def update_inventory(self, selected_items):
        self.save_inventory()


if __name__ == "__main__":
    system = KFCManagementSystem()
    system.welcome_screen()
