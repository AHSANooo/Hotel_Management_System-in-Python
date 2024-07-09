from collections import Counter
from inventory_manager import InventoryManager
from order_manager import OrderManager
from product_manager import ProductManager
from discount_manager import DiscountManager
from input_validator import InputValidator
import datetime

class CustomerInterface:
    def __init__(self):
        self.inventory_manager = InventoryManager('inventory.json', ProductManager('products.json').products)
        self.order_manager = OrderManager('orders.json')
        self.product_manager = ProductManager('products.json')
        self.customer_name = ""

    def welcome_screen(self):
        print("Welcome to KFC!\n")
        self.customer_name = input("Please enter your full name: ").strip().upper()
        while not InputValidator.validate_name(self.customer_name):
            print("\nInvalid input. Please enter a valid name.")
            self.customer_name = input("Please enter your full name: ").strip().upper()

    def get_available_items(self):
        available_items = {}
        for item, details in self.product_manager.products.items():
            if self.inventory_manager.check_availability(item):
                available_items[item] = details
        return available_items

    def select_items(self):
        selected_items = []
        available_items = self.get_available_items()

        if not available_items:
            print("\nSorry, no items are available at the moment.")
            return selected_items

        while True:
            print("\nAvailable items:")
            index = 1
            item_map = {}
            for item, details in available_items.items():
                max_qty = min(self.inventory_manager.inventory[component] // count for component, count in details['components'].items())
                price_info = f"Rs.{details['price']}"
                if 'discount' in details:
                    price_info += f" (Discount: {details['discount']}%)"
                print(f"{index}. {item}: {price_info}")
                item_map[index] = item
                index += 1

            print(f"{index}. Done")
            choice = input("\nEnter your choice (number): ").strip()
            if not InputValidator.validate_choice(choice, index):
                print("\nInvalid choice. Please enter a valid number.")
                continue

            if choice == str(index):
                break

            selected_item = item_map[int(choice)]
            max_qty = min(self.inventory_manager.inventory[component] // count for component, count in self.product_manager.products[selected_item]['components'].items())
            qty = input(f"Enter quantity for {selected_item} (Max: {max_qty}): ").strip()
            if not InputValidator.validate_quantity(qty, max_qty):
                print(f"\nInvalid quantity. Please enter a number between 1 and {max_qty}.")
                continue

            qty = int(qty)
            selected_items.extend([selected_item] * qty)

        return selected_items

    def payment_method(self):
        payment_method = input("\nEnter payment method (Card/Cash): ").strip().lower()
        while not InputValidator.validate_payment_method(payment_method):
            print("\nInvalid payment method. Please enter 'Card' or 'Cash'.")
            payment_method = input("\nEnter payment method (Card/Cash): ").strip().lower()
        return payment_method

    def get_order_count(self):
        return sum(1 for order in self.order_manager.orders if order['customer_name'] == self.customer_name)

    def apply_discounts(self, selected_items, payment_method):
        total, discount, total_after_discount = DiscountManager.apply_discounts(
            selected_items,
            self.product_manager.products,
            payment_method,
            self.get_order_count()
        )
        return total, discount, total_after_discount

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
