class DiscountManager:
    @staticmethod
    def apply_discounts(selected_items, products, payment_method, order_count):
        total = sum(products[item]['price'] for item in selected_items)
        discount = 0
        if payment_method == '1':
            payment_method = 'card'
            discount += 0.05
        elif payment_method == '2':
            payment_method = 'cash'
        if order_count > 0:
            discount += 0.027
            if order_count > 10:
                discount += 0.12
                discount -= 0.027

        for item in selected_items:
            if 'discount' in products[item]:
                item_discount = products[item]['discount'] / 100
                total -= products[item]['price'] * item_discount

        total_after_discount = total * (1 - discount)
        return total, discount, total_after_discount
