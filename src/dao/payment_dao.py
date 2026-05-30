from src.db_config import get_supabase, get_db_mode, get_sqlite_conn
from postgrest.exceptions import APIError
import sqlite3

class PaymentDAO:
    def __init__(self):
        self.mode = get_db_mode()
        if self.mode == "supabase":
            self.client = get_supabase()

    def rental_exists(self, rental_id) -> bool:
        """Check if rental_id exists in rentals table"""
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM rentals WHERE id = ?;", (rental_id,))
                row = cursor.fetchone()
                conn.close()
                return row is not None
            except Exception:
                return False
        else:
            try:
                result = self.client.table("rentals").select("id").eq("id", rental_id).execute().data
                return len(result) > 0
            except Exception:
                return False

    def customer_exists(self, customer_id) -> bool:
        """Check if customer_id exists in customers table"""
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM customers WHERE id = ?;", (customer_id,))
                row = cursor.fetchone()
                conn.close()
                return row is not None
            except Exception:
                return False
        else:
            try:
                result = self.client.table("customers").select("id").eq("id", customer_id).execute().data
                return len(result) > 0
            except Exception:
                return False

    def add_payment(self, rental_id, customer_id, amount, payment_date, payment_type):
        """Insert a new payment if rental & customer exist"""
        if not self.rental_exists(rental_id):
            return f"❌ Error: Rental ID {rental_id} not found."
        if not self.customer_exists(customer_id):
            return f"❌ Error: Customer ID {customer_id} not found."

        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO payments (rental_id, customer_id, amount, payment_date, payment_type)
                    VALUES (?, ?, ?, ?, ?);
                """, (rental_id, customer_id, amount, payment_date, payment_type))
                payment_id = cursor.lastrowid
                conn.commit()
                conn.close()
                return f"✅ Payment added successfully in SQLite. ID: {payment_id}"
            except Exception as e:
                return f"❌ SQLite Error while adding payment: {e}"
        else:
            try:
                result = self.client.table("payments").insert({
                    "rental_id": rental_id,
                    "customer_id": customer_id,
                    "amount": amount,
                    "payment_date": payment_date,
                    "payment_type": payment_type
                }).execute().data
                return f"✅ Payment added successfully: {result}"
            except APIError as e:
                return f"❌ Database error while adding payment: {e}"

    def update_payment(self, payment_id, amount=None, payment_date=None, payment_type=None):
        if self.mode == "sqlite":
            try:
                update_data = []
                query_parts = []
                if amount is not None:
                    query_parts.append("amount = ?")
                    update_data.append(amount)
                if payment_date is not None:
                    query_parts.append("payment_date = ?")
                    update_data.append(payment_date)
                if payment_type is not None:
                    query_parts.append("payment_type = ?")
                    update_data.append(payment_type)

                if not query_parts:
                    return "⚠️ No fields provided to update."

                update_data.append(payment_id)
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute(f"""
                    UPDATE payments
                    SET {", ".join(query_parts)}
                    WHERE id = ?;
                """, tuple(update_data))
                conn.commit()
                changes = conn.total_changes
                conn.close()

                if changes > 0:
                    return f"✅ Payment ID {payment_id} updated successfully in SQLite."
                return f"⚠️ Payment ID {payment_id} not found."
            except Exception as e:
                return f"❌ SQLite Error while updating payment: {e}"
        else:
            try:
                update_data = {}
                if amount is not None: update_data["amount"] = amount
                if payment_date is not None: update_data["payment_date"] = payment_date
                if payment_type is not None: update_data["payment_type"] = payment_type

                if not update_data:
                    return "⚠️ No fields provided to update."

                result = self.client.table("payments").update(update_data).eq("id", payment_id).execute().data
                if result:
                    return f"✅ Payment updated: {result}"
                return f"⚠️ Payment ID {payment_id} not found."
            except APIError as e:
                return f"❌ Database error while updating payment: {e}"

    def delete_payment(self, payment_id):
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM payments WHERE id = ?;", (payment_id,))
                conn.commit()
                changes = conn.total_changes
                conn.close()
                if changes > 0:
                    return f"🗑️ Payment {payment_id} deleted successfully from SQLite."
                return f"⚠️ Payment ID {payment_id} not found."
            except Exception as e:
                return f"❌ SQLite Error while deleting payment: {e}"
        else:
            try:
                result = self.client.table("payments").delete().eq("id", payment_id).execute().data
                if result:
                    return f"🗑️ Payment {payment_id} deleted successfully."
                return f"⚠️ Payment ID {payment_id} not found."
            except APIError as e:
                return f"❌ Database error while deleting payment: {e}"

    def list_payments(self):
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT p.id, p.rental_id, p.customer_id, p.amount, p.payment_date, p.payment_type, p.created_at,
                           c.name as customer_name, c.email as customer_email,
                           v.plate as vehicle_plate, v.model as vehicle_model
                    FROM payments p
                    LEFT JOIN customers c ON p.customer_id = c.id
                    LEFT JOIN rentals r ON p.rental_id = r.id
                    LEFT JOIN vehicles v ON r.vehicle_id = v.id
                    ORDER BY p.id DESC;
                """)
                rows = cursor.fetchall()
                conn.close()
                return [dict(r) for r in rows]
            except Exception as e:
                return f"❌ SQLite Error while fetching payments: {e}"
        else:
            try:
                result = self.client.table("payments").select("*, customers(*), rentals(*, vehicles(*))").execute().data
                flat_results = []
                for p in (result if result else []):
                    flat_p = p.copy()
                    if "customers" in p and isinstance(p["customers"], dict):
                        flat_p["customer_name"] = p["customers"].get("name")
                        flat_p["customer_email"] = p["customers"].get("email")
                    if "rentals" in p and isinstance(p["rentals"], dict):
                        rental = p["rentals"]
                        if "vehicles" in rental and isinstance(rental["vehicles"], dict):
                            flat_p["vehicle_plate"] = rental["vehicles"].get("plate")
                            flat_p["vehicle_model"] = rental["vehicles"].get("model")
                    flat_results.append(flat_p)
                return flat_results
            except APIError as e:
                return f"❌ Database error while fetching payments: {e}"

    def search_payment(self, payment_id):
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT p.id, p.rental_id, p.customer_id, p.amount, p.payment_date, p.payment_type, p.created_at,
                           c.name as customer_name, c.email as customer_email,
                           v.plate as vehicle_plate, v.model as vehicle_model
                    FROM payments p
                    LEFT JOIN customers c ON p.customer_id = c.id
                    LEFT JOIN rentals r ON p.rental_id = r.id
                    LEFT JOIN vehicles v ON r.vehicle_id = v.id
                    WHERE p.id = ?;
                """, (payment_id,))
                row = cursor.fetchone()
                conn.close()
                return [dict(row)] if row else f"⚠️ Payment ID {payment_id} not found."
            except Exception as e:
                return f"❌ SQLite Error while searching payment: {e}"
        else:
            try:
                result = (
                    self.client.table("payments")
                    .select("*, customers(*), rentals(*, vehicles(*))")
                    .eq("id", payment_id)
                    .execute()
                    .data
                )
                if result:
                    p = result[0]
                    flat_p = p.copy()
                    if "customers" in p and isinstance(p["customers"], dict):
                        flat_p["customer_name"] = p["customers"].get("name")
                        flat_p["customer_email"] = p["customers"].get("email")
                    if "rentals" in p and isinstance(p["rentals"], dict):
                        rental = p["rentals"]
                        if "vehicles" in rental and isinstance(rental["vehicles"], dict):
                            flat_p["vehicle_plate"] = rental["vehicles"].get("plate")
                            flat_p["vehicle_model"] = rental["vehicles"].get("model")
                    return [flat_p]
                return f"⚠️ Payment ID {payment_id} not found."
            except APIError as e:
                return f"❌ Database error while searching payment: {e}"
