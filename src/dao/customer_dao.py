from src.db_config import get_supabase, get_db_mode, get_sqlite_conn
from postgrest.exceptions import APIError
import sqlite3

class CustomerDAO:
    """Data Access Object (DAO) for managing customer records in Supabase and SQLite."""

    def __init__(self):
        self.mode = get_db_mode()
        if self.mode == "supabase":
            self.client = get_supabase()

    def add_customer(self, name, email, phone, license_no="", address=""):
        """Insert a new customer record."""
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO customers (name, email, phone, license_no, address)
                    VALUES (?, ?, ?, ?, ?);
                """, (name, email, phone, license_no, address))
                conn.commit()
                row_id = cursor.lastrowid
                conn.close()
                return f"✅ Customer added successfully in SQLite. ID: {row_id}"
            except sqlite3.IntegrityError as e:
                return f"❌ Email '{email}' already registered: {e}"
            except Exception as e:
                return f"❌ SQLite Error while adding customer: {e}"
        else:
            try:
                result = (
                    self.client.table("customers")
                    .insert({
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "license_no": license_no,
                        "address": address
                    })
                    .execute()
                    .data
                )
                return f"✅ Customer added successfully: {result}"
            except APIError as e:
                # Fallback in case columns do not exist in some environments
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
                    return f"✅ Customer added successfully (without extra columns): {result}"
                except APIError as e2:
                    return f"❌ Database Error while adding customer: {e2}"

    def update_customer(self, customer_id, name=None, email=None, phone=None, license_no=None, address=None):
        """Update existing customer details."""
        if self.mode == "sqlite":
            try:
                update_data = []
                query_parts = []
                if name is not None:
                    query_parts.append("name = ?")
                    update_data.append(name)
                if email is not None:
                    query_parts.append("email = ?")
                    update_data.append(email)
                if phone is not None:
                    query_parts.append("phone = ?")
                    update_data.append(phone)
                if license_no is not None:
                    query_parts.append("license_no = ?")
                    update_data.append(license_no)
                if address is not None:
                    query_parts.append("address = ?")
                    update_data.append(address)

                if not query_parts:
                    return "⚠️ No fields provided for update."

                update_data.append(customer_id)
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute(f"""
                    UPDATE customers
                    SET {", ".join(query_parts)}
                    WHERE id = ?;
                """, tuple(update_data))
                conn.commit()
                changes = conn.total_changes
                conn.close()

                if changes > 0:
                    return f"✅ Customer ID {customer_id} updated successfully in SQLite."
                return f"⚠️ Customer ID {customer_id} not found."
            except sqlite3.IntegrityError as e:
                return f"❌ Email already registered: {e}"
            except Exception as e:
                return f"❌ SQLite Error while updating customer: {e}"
        else:
            try:
                update_data = {}
                if name is not None: update_data["name"] = name
                if email is not None: update_data["email"] = email
                if phone is not None: update_data["phone"] = phone
                if license_no is not None: update_data["license_no"] = license_no
                if address is not None: update_data["address"] = address

                if not update_data:
                    return "⚠️ No fields provided for update."

                result = (
                    self.client.table("customers")
                    .update(update_data)
                    .eq("id", customer_id)
                    .execute()
                    .data
                )

                if result:
                    return f"✅ Customer updated successfully: {result}"
                return f"⚠️ Customer ID {customer_id} not found."

            except APIError as e:
                return f"❌ Database Error while updating customer: {e}"

    def delete_customer(self, customer_id):
        """Delete a customer record by ID."""
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM customers WHERE id = ?;", (customer_id,))
                conn.commit()
                changes = conn.total_changes
                conn.close()
                if changes > 0:
                    return f"🗑️ Customer {customer_id} deleted successfully from SQLite."
                return f"⚠️ Customer ID {customer_id} not found."
            except Exception as e:
                return f"❌ SQLite Error while deleting customer: {e}"
        else:
            try:
                result = (
                    self.client.table("customers")
                    .delete()
                    .eq("id", customer_id)
                    .execute()
                    .data
                )

                if result:
                    return f"🗑️ Customer {customer_id} deleted successfully."
                return f"⚠️ Customer ID {customer_id} not found."

            except APIError as e:
                return f"❌ Database Error while deleting customer: {e}"

    def list_customers(self):
        """Retrieve all customers."""
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM customers ORDER BY id DESC;")
                rows = cursor.fetchall()
                conn.close()
                return [dict(r) for r in rows]
            except Exception as e:
                return f"❌ SQLite Error while fetching customers: {e}"
        else:
            try:
                result = self.client.table("customers").select("*").execute().data
                return result if result else []
            except APIError as e:
                return f"❌ Database Error while fetching customers: {e}"

    def search_customer(self, customer_id):
        """Search for a customer by ID."""
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM customers WHERE id = ?;", (customer_id,))
                row = cursor.fetchone()
                conn.close()
                return [dict(row)] if row else f"⚠️ Customer ID {customer_id} not found."
            except Exception as e:
                return f"❌ SQLite Error while searching customer: {e}"
        else:
            try:
                result = (
                    self.client.table("customers")
                    .select("*")
                    .eq("id", customer_id)
                    .execute()
                    .data
                )
                return result if result else f"⚠️ Customer ID {customer_id} not found."
            except APIError as e:
                return f"❌ Database Error while searching customer: {e}"