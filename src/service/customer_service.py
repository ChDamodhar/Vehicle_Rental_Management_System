from src.dao.customer_dao import CustomerDAO

class CustomerService:
    """Service layer for managing customer operations."""

    def __init__(self):
        self.dao = CustomerDAO()

    def add_customer(self, name, email, phone, license_no="", address=""):
        """Add a new customer with input validation."""
        if not name or not name.strip():
            return "❌ Error: Customer Name cannot be empty."
        if not email or not email.strip() or "@" not in email:
            return "❌ Error: A valid Email address is required."
        
        return self.dao.add_customer(
            name.strip(), 
            email.strip(), 
            phone.strip() if phone else "", 
            license_no.strip() if license_no else "", 
            address.strip() if address else ""
        )

    def update_customer(self, customer_id, name=None, email=None, phone=None, license_no=None, address=None):
        """Update an existing customer's details with input validation."""
        if not customer_id:
            return "❌ Error: Customer ID is required for updates."
        
        if email is not None:
            if not email.strip() or "@" not in email:
                return "❌ Error: A valid Email address is required."
            email = email.strip()

        return self.dao.update_customer(
            customer_id,
            name.strip() if name is not None else None,
            email,
            phone.strip() if phone is not None else None,
            license_no.strip() if license_no is not None else None,
            address.strip() if address is not None else None
        )

    def delete_customer(self, customer_id):
        """Delete a customer by ID."""
        if not customer_id:
            return "❌ Error: Customer ID is required."
        return self.dao.delete_customer(customer_id)

    def list_customers(self):
        """List all customers."""
        return self.dao.list_customers()

    def search_customer(self, customer_id):
        """Search for a customer by ID."""
        if not customer_id:
            return "❌ Error: Customer ID is required."
        return self.dao.search_customer(customer_id)