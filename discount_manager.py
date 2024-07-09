class DiscountManager:
    def __init__(self):
        self.payment_method_discounts = {'card': 0.05, 'cash': 0.0}
        self.order_count_discounts = {1: 0.027, 11: 0.12}
        self.item_discounts = {}

    @staticmethod
    def apply_discounts(selected_items, products, payment_method, order_count):
        total = sum(products[item]['price'] for item in selected_items)
        discount = 0

        # Apply payment method discount
        if payment_method == '1':
            payment_method = 'card'
            discount += 0.05
        elif payment_method == '2':
            payment_method = 'cash'

        # Apply order count discounts
        if order_count > 0:
            discount += 0.027
            if order_count > 10:
                discount += 0.12 - 0.027

        # Apply product-specific discounts
        for item in selected_items:
            if 'discount' in products[item]:
                item_discount = products[item]['discount'] / 100
                total -= products[item]['price'] * item_discount

        total_after_discount = total * (1 - discount)
        return total, discount, total_after_discount

    def set_payment_method_discount(self, payment_method, discount):
        self.payment_method_discounts[payment_method] = discount

    def set_order_count_discount(self, count_threshold, discount):
        self.order_count_discounts[count_threshold] = discount

    def set_item_discount(self, item, discount):
        self.item_discounts[item] = discount