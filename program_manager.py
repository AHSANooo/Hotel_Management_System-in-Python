from datetime import datetime
from customer_interface import CustomerInterface

class ProgramManager:
    def __init__(self):
        self.customer_interface = CustomerInterface()

    def run(self):
        self.customer_interface.welcome_screen()
        selected_items = self.customer_interface.select_items()
        if selected_items:
            payment_method = self.customer_interface.payment_method()
            total, discount, total_after_discount = self.customer_interface.apply_discounts(selected_items, payment_method)
            self.customer_interface.store_order(selected_items, payment_method, total_after_discount, discount, total)

if __name__ == "__main__":
    program = ProgramManager()
    program.run()
