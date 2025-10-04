# src/dao/customer_dao.py

from src.db_config import get_supabase
from postgrest.exceptions import APIError

class CustomerDAO:
    def __init__(self):
        self.client = get_supabase()

    def add_customer(self, name, email, phone, license_no, address):
        try:
            result = self.client.table("customers").insert({
                "name": name,
                "email": email,
                "phone": phone,
                "license_no": license_no,
                "address": address
            }).execute().data
            return f"✅ Customer added: {result}"
        except APIError as e:
            return f"❌ Database Error while adding customer: {e}"

    def update_customer(self, customer_id, name=None, email=None, phone=None, address=None):
        try:
            update_data = {}
            if name: update_data["name"] = name
            if email: update_data["email"] = email
            if phone: update_data["phone"] = phone
            if address: update_data["address"] = address

            if not update_data:
                return "⚠️ No fields to update."

            result = self.client.table("customers").update(update_data).eq("id", customer_id).execute().data
            if result:
                return f"✅ Customer updated: {result}"
            return f"⚠️ Customer ID {customer_id} not found."
        except APIError as e:
            return f"❌ Database Error while updating customer: {e}"

    def delete_customer(self, customer_id):
        try:
            result = self.client.table("customers").delete().eq("id", customer_id).execute().data
            if result:
                return f"🗑️ Customer {customer_id} deleted."
            return f"⚠️ Customer ID {customer_id} not found."
        except APIError as e:
            return f"❌ Database Error while deleting customer: {e}"

    def list_customers(self):
        try:
            return self.client.table("customers").select("*").execute().data
        except APIError as e:
            return f"❌ Database Error while fetching customers: {e}"

    def search_customer(self, customer_id):
        try:
            result = self.client.table("customers").select("*").eq("id", customer_id).execute().data
            return result if result else f"⚠️ Customer ID {customer_id} not found."
        except APIError as e:
            return f"❌ Database Error while searching customer: {e}"