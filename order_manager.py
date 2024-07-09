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

    def get_all_orders(self):
        return self.orders

    def get_orders_by_customer(self, customer_name):
        return [order for order in self.orders if order['customer_name'] == customer_name]

    def get_orders_by_date_range(self, start_date, end_date):
        start_date = datetime.fromisoformat(start_date)
        end_date = datetime.fromisoformat(end_date)
        return [order for order in self.orders if start_date <= datetime.fromisoformat(order['datetime']) <= end_date]

    def remove_order(self, order_index):
        if 0 <= order_index < len(self.orders):
            del self.orders[order_index]
            self.save_orders()
        else:
            print("Invalid order index.")

    def update_order(self, order_index, new_details):
        if 0 <= order_index < len(self.orders):
            self.orders[order_index].update(new_details)
            self.save_orders()
        else:
            print("Invalid order index.")