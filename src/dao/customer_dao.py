from src.db_config import get_supabase
from postgrest.exceptions import APIError


class CustomerDAO:
    """Data Access Object (DAO) for managing customer records in Supabase."""

    def __init__(self):
        self.client = get_supabase()

    def add_customer(self, name, email, phone):
        """Insert a new customer record."""
        try:
            result = (
                self.client.table("customers")
                .insert({
                    "name": name,
                    "email": email,
                    "phone": phone
                })
                .execute()
                .data
            )
            return f"Customer added successfully: {result}"
        except APIError as e:
            return f"Database Error while adding customer: {e}"

    def update_customer(self, customer_id, name=None, email=None, phone=None):
        """Update existing customer details."""
        try:
            update_data = {}
            if name:
                update_data["name"] = name
            if email:
                update_data["email"] = email
            if phone:
                update_data["phone"] = phone

            if not update_data:
                return "No fields provided for update."

            result = (
                self.client.table("customers")
                .update(update_data)
                .eq("id", customer_id)
                .execute()
                .data
            )

            if result:
                return f"Customer updated successfully: {result}"
            return f"Customer ID {customer_id} not found."

        except APIError as e:
            return f"Database Error while updating customer: {e}"

    def delete_customer(self, customer_id):
        """Delete a customer record by ID."""
        try:
            result = (
                self.client.table("customers")
                .delete()
                .eq("id", customer_id)
                .execute()
                .data
            )

            if result:
                return f"Customer {customer_id} deleted successfully."
            return f"Customer ID {customer_id} not found."

        except APIError as e:
            return f"Database Error while deleting customer: {e}"

    def list_customers(self):
        """Retrieve all customers."""
        try:
            result = self.client.table("customers").select("*").execute().data
            return result if result else "No customers found."
        except APIError as e:
            return f"Database Error while fetching customers: {e}"

    def search_customer(self, customer_id):
        """Search for a customer by ID."""
        try:
            result = (
                self.client.table("customers")
                .select("*")
                .eq("id", customer_id)
                .execute()
                .data
            )
            return result if result else f"Customer ID {customer_id} not found."
        except APIError as e:
            return f"Database Error while searching customer: {e}"