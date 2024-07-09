"""
import json
from datetime import datetime

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
"""

import json
from datetime import datetime

class OrderManager:
    def __init__(self, orders_file):
        self.orders_file = orders_file
        self.load_orders()

    def load_orders(self):
        try:
            with open(self.orders_file) as file:
                self.orders = json.load(file)
        except FileNotFoundError:
            self.orders = []

    def save_orders(self):
        with open(self.orders_file, 'w') as file:
            json.dump(self.orders, file, indent=4)

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
