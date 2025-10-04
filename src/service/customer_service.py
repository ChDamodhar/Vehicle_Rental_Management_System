from src.dao.customer_dao import CustomerDAO


class CustomerService:
    """Service layer for managing customer operations."""

    def __init__(self):
        self.dao = CustomerDAO()

    def add_customer(self, name, email, phone):
        """Add a new customer."""
        return self.dao.add_customer(name, email, phone)

    def update_customer(self, customer_id, name=None, email=None, phone=None):
        """Update an existing customer's details."""
        return self.dao.update_customer(customer_id, name, email, phone)

    def delete_customer(self, customer_id):
        """Delete a customer by ID."""
        return self.dao.delete_customer(customer_id)

    def list_customers(self):
        """List all customers."""
        return self.dao.list_customers()

    def search_customer(self, customer_id):
        """Search for a customer by ID."""
        return self.dao.search_customer(customer_id)