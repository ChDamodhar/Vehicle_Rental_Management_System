from src.db_config import get_supabase

class PaymentDAO:
    def __init__(self):
        self.client = get_supabase()

    def rental_exists(self, rental_id: int) -> bool:
        """Check if rental_id exists in rentals table"""
        result = self.client.table("rentals").select("id").eq("id", rental_id).execute().data
        return len(result) > 0

    def customer_exists(self, customer_id: int) -> bool:
        """Check if customer_id exists in customers table"""
        result = self.client.table("customers").select("id").eq("id", customer_id).execute().data
        return len(result) > 0

    def add_payment(self, rental_id, customer_id, amount, payment_date, payment_type):
        """Insert a new payment if rental & customer exist"""
        if not self.rental_exists(rental_id):
            return f"❌ Error: Rental ID {rental_id} not found."
        if not self.customer_exists(customer_id):
            return f"❌ Error: Customer ID {customer_id} not found."

        result = self.client.table("payments").insert({
            "rental_id": rental_id,
            "customer_id": customer_id,
            "amount": amount,
            "payment_date": payment_date,
            "payment_type": payment_type
        }).execute().data
        return f"✅ Payment added successfully: {result}"

    def update_payment(self, payment_id, amount=None, payment_date=None, payment_type=None):
        update_data = {}
        if amount: update_data["amount"] = amount
        if payment_date: update_data["payment_date"] = payment_date
        if payment_type: update_data["payment_type"] = payment_type

        result = self.client.table("payments").update(update_data).eq("id", payment_id).execute().data
        return f"✅ Payment updated: {result}"

    def delete_payment(self, payment_id):
        self.client.table("payments").delete().eq("id", payment_id).execute()
        return f"🗑️ Payment {payment_id} deleted successfully."

    def list_payments(self):
        return self.client.table("payments").select("*").execute().data

    def search_payment(self, payment_id):
        return self.client.table("payments").select("*").eq("id", payment_id).execute().data
