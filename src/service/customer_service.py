from src.dao.customer_dao import CustomerDAO

class CustomerService:
    def __init__(self):
        self.dao = CustomerDAO()

    def add_customer(self, name, email, phone, license_no, address):
        return self.dao.add_customer(name, email, phone, license_no, address)

    def update_customer(self, customer_id, name=None, email=None, phone=None, address=None):
        fields = {k: v for k, v in {"name": name, "email": email, "phone": phone, "address": address}.items() if v}
        return self.dao.update_customer(customer_id, fields)

    def delete_customer(self, customer_id):
        return self.dao.delete_customer(customer_id)

    def list_customers(self):
        return self.dao.list_customers()

    def search_customer(self, keyword):
        return self.dao.search_customer(keyword)
