import json
import re
from collections import Counter
from datetime import datetime
from inventory_manager import InventoryManager
from order_manager import OrderManager

class KFCManagementSystem:
    def __init__(self):
        self.order_manager = OrderManager('orders.json')
        self.products_file = 'products.json'
        self.load_products()

    def load_products(self):
        try:
            with open(self.products_file) as file:
                self.products = json.load(file)
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
        available_items = {item: details for item, details in self.products.items() if self.inventory_manager.check_availability(item)}
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
                max_qty = min(self.inventory_manager.inventory[component] // count for component, count in
                              details['components'].items())
                price_info = f"Rs.{details['price']}"
                if 'discount' in details:
                    price_info += f" (Discount: {details['discount']}%)"
                print(f"{index}. {item}: {price_info} ")
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
            max_qty = min(self.inventory_manager.inventory[component] // count for component, count in
                          self.products[selected_item]['components'].items())
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

    def payment_method(self, selected_items):
        print("\nPayment Methods:")
        print("1. Card")
        print("2. Cash")
        choice = input("Enter your choice (number): ").strip()
        if choice == "1":
            payment_method = "card"
        elif choice == "2":
            payment_method = "cash"
        else:
            print("\nInvalid choice. Please enter '1' or '2'.")
            return self.payment_method(selected_items)
        self.apply_discounts(selected_items, payment_method)

    def get_order_count(self):
        return sum(1 for order in self.order_manager.orders if order['customer_name'] == self.customer_name)

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

        # Apply product-specific discounts
        for item in selected_items:
            if 'discount' in self.products[item]:
                item_discount = self.products[item]['discount'] / 100
                total -= self.products[item]['price'] * item_discount

        total_after_discount = total * (1 - discount)
        self.store_order(selected_items, payment_method, total_after_discount, discount, total)

    def store_order(self, selected_items, payment_method, total_after_discount, total_discount, total):
        self.order_manager.place_order(self.customer_name, selected_items, payment_method, total, total_discount, total_after_discount)
        item_summary = Counter(selected_items)
        item_summary_str = ', '.join(f"{item} x {count}" for item, count in item_summary.items())
        print("Order placed successfully!")
        print(f"Customer_name : {self.customer_name}")
        print(f"Items : {item_summary_str}")
        print(f"Payment Method :  {payment_method}")
        print(f"Bill : Rs.{total}/-")
        print(f"Discount : {total_discount * 100}%")
        print(f"Total amount to be paid: Rs.{total_after_discount:.2f}/.")
        print(f"Date and time : {datetime.now().date()}   {datetime.now().strftime('%H:%M')}")

        self.inventory_manager.update_inventory(selected_items)
