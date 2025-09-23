from src.dao.payment_dao import PaymentDAO

class PaymentService:
    def __init__(self):
        self.dao = PaymentDAO()

    def add_payment(self, rental_id, customer_id, amount, payment_date, payment_type):
        return self.dao.add_payment(rental_id, customer_id, amount, payment_date, payment_type)

    def update_payment(self, payment_id, amount=None, payment_date=None, payment_type=None):
        return self.dao.update_payment(payment_id, amount, payment_date, payment_type)

    def delete_payment(self, payment_id):
        return self.dao.delete_payment(payment_id)

    def list_payments(self):
        return self.dao.list_payments()

    def search_payment(self, payment_id):
        return self.dao.search_payment(payment_id)
