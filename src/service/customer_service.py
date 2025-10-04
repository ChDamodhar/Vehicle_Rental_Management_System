# src/service/customer_service.py

from src.dao.customer_dao import CustomerDAO

class CustomerService:
    def __init__(self):
        self.dao = CustomerDAO()

    def add_customer(self, name, email, phone, license_no, address):
        return self.dao.add_customer(name, email, phone, license_no, address)

    def update_customer(self, customer_id, name=None, email=None, phone=None, address=None):
        return self.dao.update_customer(customer_id, name, email, phone, address)

    def delete_customer(self, customer_id):
        return self.dao.delete_customer(customer_id)

    def list_customers(self):
        return self.dao.list_customers()

    def search_customer(self, customer_id):
        return self.dao.search_customer(customer_id)