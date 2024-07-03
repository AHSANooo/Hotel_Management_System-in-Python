import json
import re
from datetime import datetime

class KFCManagementSystem:
    def __init__(self):
        self.inventory_file = 'inventory.txt'
        self.orders_file = 'orders.txt'
        self.customers_file = 'customers.txt'
        self.load_inventory()
        self.load_customers()
        self.load_orders()

    def load_inventory(self):
        try:
            with open(self.inventory_file, 'r') as file:
                self.inventory = json.loads(file.read())
        except FileNotFoundError:
            self.inventory = {}

    def save_inventory(self):
        with open(self.inventory_file, 'w') as file:
            file.write(json.dumps(self.inventory))

    def load_customers(self):
        try:
            with open(self.customers_file, 'r') as file:
                self.customers = json.loads(file.read())
        except FileNotFoundError:
            self.customers = {}

    def save_customers(self):
        with open(self.customers_file, 'w') as file:
            file.write(json.dumps(self.customers))

    def load_orders(self):
        try:
            with open(self.orders_file, 'r') as file:
                self.orders = json.loads(file.read())
        except FileNotFoundError:
            self.orders = []

    def save_orders(self):
        with open(self.orders_file, 'w') as file:
            file.write(json.dumps(self.orders))

    def welcome_screen(self):
        print("Welcome to KFC!")
        self.customer_name = input("Please enter your full name: ")
        if not re.match("^[A-Za-z ]+$", self.customer_name):
            print("Invalid input. Please enter a valid name.")
            return self.welcome_screen()
        self.check_inventory()

    def check_inventory(self):
        available_items = {item: details for item, details in self.inventory.items() if all(count > 0 for count in details['components'].values())}
        if not available_items:
            print("Sorry, no items are available at the moment.")
            return
        print("Available items:")
        for item, details in available_items.items():
            print(f"{item}: Rs.{details['price']}")
        self.order_items = self.select_items(available_items)

    def select_items(self, available_items):
        selected_items = []
        while True:
            item = input("Enter item name to add to your order (or type 'done' to finish): ").strip().lower()
            if item == 'done':
                break
            if item in available_items:
                selected_items.append(item)
            else:
                print("Item not available. Please choose from the available items.")
        if not selected_items:
            print("No items selected. Please select at least one item.")
            return self.select_items(available_items)
        self.payment_method(selected_items)

    def payment_method(self, selected_items):
        payment_method = input("Enter payment method (Card/Cash): ").strip().lower()
        if payment_method not in ['card', 'cash']:
            print("Invalid payment method. Please enter 'Card' or 'Cash'.")
            return self.payment_method(selected_items)
        self.apply_discounts(selected_items, payment_method)

    def apply_discounts(self, selected_items, payment_method):
        total = sum(self.inventory[item]['price'] for item in selected_items)
        discount = 0
        if payment_method == 'card':
            discount += 0.05
        if self.customer_name in self.customers:
            discount += 0.027
            if self.customers[self.customer_name] > 10:
                discount += 0.12
        total_after_discount = total * (1 - discount)
        self.store_order(selected_items, payment_method, total_after_discount,discount,total)

    def store_order(self, selected_items, payment_method, total_after_discount,total_discount,total):
        order = {
            'customer_name': self.customer_name,
            'items': selected_items,
            'payment_method': payment_method,
            'total': total_after_discount,
            'datetime': datetime.now().isoformat()
        }
        self.orders.append(order)
        self.save_orders()
        if self.customer_name in self.customers:
            self.customers[self.customer_name] += 1
        else:
            self.customers[self.customer_name] = 1
        self.save_customers()
        print("Order placed successfully!")
        print(f"Customer_name : {self.customer_name}")
        print(f"Items : {selected_items}")
        print(f"Payment Method :  {payment_method}")
        print(f"Total : {total_after_discount}")
        print(f"Bill : {total}")
        print(f"Discount : {total_discount*100}%")
        print(f"Total amount to be paid: ${total_after_discount:.2f}")
        print(f"Date and time : {datetime.now().isoformat()}")

        self.update_inventory(selected_items)

    def update_inventory(self, selected_items):
        for item in selected_items:
            for component, count in self.inventory[item]['components'].items():
                self.inventory[component] -= count
        self.save_inventory()

if __name__ == "__main__":
    system = KFCManagementSystem()
    system.welcome_screen()
