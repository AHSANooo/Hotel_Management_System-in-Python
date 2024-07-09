import re

class InputValidator:
    @staticmethod
    def validate_name(name):
        return re.match("^[A-Za-z ]+$", name) is not None

    @staticmethod
    def validate_choice(choice, options):
        return choice.isdigit() and 1 <= int(choice) <= options

    @staticmethod
    def validate_quantity(qty, max_qty):
        return qty.isdigit() and 1 <= int(qty) <= max_qty

    @staticmethod
    def validate_payment_method(payment_method):
        return payment_method in ['1', '2']
