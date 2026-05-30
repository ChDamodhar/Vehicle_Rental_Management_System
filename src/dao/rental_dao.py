from src.db_config import get_supabase, get_db_mode, get_sqlite_conn
from postgrest.exceptions import APIError
import sqlite3

class RentalDAO:
    def __init__(self):
        self.mode = get_db_mode()
        if self.mode == "supabase":
            self.client = get_supabase()

    def is_vehicle_available(self, vehicle_id):
        """Checks if a vehicle is currently marked as available."""
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("SELECT available FROM vehicles WHERE id = ?;", (vehicle_id,))
                row = cursor.fetchone()
                conn.close()
                if row:
                    return bool(row["available"])
                return False
            except Exception:
                return False
        else:
            try:
                res = self.client.table("vehicles").select("available").eq("id", vehicle_id).execute().data
                if res:
                    return bool(res[0].get("available", False))
                return False
            except Exception:
                return False

    def add_rental(self, vehicle_id, customer_id, start_date, end_date):
        """Add a new rental record and mark the vehicle as rented (unavailable)."""
        # Validate vehicle availability first
        if not self.is_vehicle_available(vehicle_id):
            return f"❌ Error: Vehicle ID '{vehicle_id}' is not available (either already rented or in maintenance)."

        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                
                # Check customer existence
                cursor.execute("SELECT id FROM customers WHERE id = ?;", (customer_id,))
                if not cursor.fetchone():
                    conn.close()
                    return f"❌ Error: Customer ID '{customer_id}' does not exist."

                # Insert rental
                cursor.execute("""
                    INSERT INTO rentals (vehicle_id, customer_id, start_date, end_date)
                    VALUES (?, ?, ?, ?);
                """, (vehicle_id, customer_id, start_date, end_date))
                rental_id = cursor.lastrowid
                
                # Set vehicle availability to False (rented)
                cursor.execute("UPDATE vehicles SET available = 0 WHERE id = ?;", (vehicle_id,))
                
                conn.commit()
                conn.close()
                return f"✅ Rental added successfully in SQLite. ID: {rental_id} (Vehicle marked Rented)"
            except Exception as e:
                return f"❌ SQLite Error while adding rental: {e}"
        else:
            try:
                result = (
                    self.client.table("rentals")
                    .insert({
                        "vehicle_id": vehicle_id,
                        "customer_id": customer_id,
                        "start_date": start_date,
                        "end_date": end_date
                    })
                    .execute()
                    .data
                )
                if result:
                    # Set vehicle availability to False
                    self.client.table("vehicles").update({"available": False}).eq("id", vehicle_id).execute()
                    return f"✅ Rental added successfully: {result}"
                return f"❌ Failed to insert rental in cloud."
            except APIError as e:
                return f"❌ Database error while adding rental: {e}"

    def update_rental(self, rental_id, start_date=None, end_date=None):
        """Update rental dates."""
        if self.mode == "sqlite":
            try:
                update_data = []
                query_parts = []
                if start_date:
                    query_parts.append("start_date = ?")
                    update_data.append(start_date)
                if end_date:
                    query_parts.append("end_date = ?")
                    update_data.append(end_date)

                if not query_parts:
                    return "⚠️ No fields provided to update."

                update_data.append(rental_id)
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute(f"""
                    UPDATE rentals
                    SET {", ".join(query_parts)}
                    WHERE id = ?;
                """, tuple(update_data))
                conn.commit()
                changes = conn.total_changes
                conn.close()

                if changes > 0:
                    return f"✅ Rental ID {rental_id} updated successfully in SQLite."
                return f"⚠️ Rental ID {rental_id} not found."
            except Exception as e:
                return f"❌ SQLite Error while updating rental: {e}"
        else:
            try:
                update_data = {}
                if start_date: update_data["start_date"] = start_date
                if end_date: update_data["end_date"] = end_date

                if not update_data:
                    return "⚠️ No fields provided to update."

                result = (
                    self.client.table("rentals")
                    .update(update_data)
                    .eq("id", rental_id)
                    .execute()
                    .data
                )
                if result:
                    return f"✅ Rental updated: {result}"
                return f"⚠️ Rental ID {rental_id} not found."
            except APIError as e:
                return f"❌ Database error while updating rental: {e}"

    def delete_rental(self, rental_id):
        """Delete a rental record by ID and mark its vehicle as available again."""
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                
                # Fetch vehicle_id before deleting the rental
                cursor.execute("SELECT vehicle_id FROM rentals WHERE id = ?;", (rental_id,))
                row = cursor.fetchone()
                if not row:
                    conn.close()
                    return f"⚠️ Rental ID {rental_id} not found."
                
                vehicle_id = row["vehicle_id"]
                
                # Delete rental
                cursor.execute("DELETE FROM rentals WHERE id = ?;", (rental_id,))
                
                # Restore vehicle availability to True (available)
                cursor.execute("UPDATE vehicles SET available = 1 WHERE id = ?;", (vehicle_id,))
                
                conn.commit()
                conn.close()
                return f"🗑️ Rental {rental_id} deleted successfully. Vehicle {vehicle_id} is now available."
            except Exception as e:
                return f"❌ SQLite Error while deleting rental: {e}"
        else:
            try:
                # Find vehicle_id first
                rental_data = self.client.table("rentals").select("vehicle_id").eq("id", rental_id).execute().data
                if not rental_data:
                    return f"⚠️ Rental ID {rental_id} not found."
                
                vehicle_id = rental_data[0].get("vehicle_id")
                
                result = (
                    self.client.table("rentals")
                    .delete()
                    .eq("id", rental_id)
                    .execute()
                    .data
                )
                if result:
                    # Restore vehicle availability
                    self.client.table("vehicles").update({"available": True}).eq("id", vehicle_id).execute()
                    return f"🗑️ Rental {rental_id} deleted successfully. Vehicle {vehicle_id} marked available."
                return f"⚠️ Rental ID {rental_id} not found."
            except APIError as e:
                return f"❌ Database error while deleting rental: {e}"

    def list_rentals(self):
        """Retrieve all rentals with detailed customer and vehicle info."""
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT r.id, r.vehicle_id, r.customer_id, r.start_date, r.end_date, r.created_at,
                           v.plate as vehicle_plate, v.model as vehicle_model, v.rate as vehicle_rate,
                           c.name as customer_name, c.email as customer_email, c.phone as customer_phone
                    FROM rentals r
                    LEFT JOIN vehicles v ON r.vehicle_id = v.id
                    LEFT JOIN customers c ON r.customer_id = c.id
                    ORDER BY r.id DESC;
                """)
                rows = cursor.fetchall()
                conn.close()
                return [dict(r) for r in rows]
            except Exception as e:
                return f"❌ SQLite Error while fetching rentals: {e}"
        else:
            try:
                # Simple select in Supabase, client-side join can be handled or standard API query
                result = self.client.table("rentals").select("*, vehicles(*), customers(*)").execute().data
                # Standardize nested structure if returned
                flat_results = []
                for r in (result if result else []):
                    flat_r = r.copy()
                    if "vehicles" in r and isinstance(r["vehicles"], dict):
                        flat_r["vehicle_plate"] = r["vehicles"].get("plate")
                        flat_r["vehicle_model"] = r["vehicles"].get("model")
                        flat_r["vehicle_rate"] = r["vehicles"].get("rate")
                    if "customers" in r and isinstance(r["customers"], dict):
                        flat_r["customer_name"] = r["customers"].get("name")
                        flat_r["customer_email"] = r["customers"].get("email")
                        flat_r["customer_phone"] = r["customers"].get("phone")
                    flat_results.append(flat_r)
                return flat_results
            except APIError as e:
                return f"❌ Database error while fetching rentals: {e}"

    def search_rental(self, rental_id):
        """Search rental by ID with relations."""
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT r.id, r.vehicle_id, r.customer_id, r.start_date, r.end_date, r.created_at,
                           v.plate as vehicle_plate, v.model as vehicle_model, v.rate as vehicle_rate,
                           c.name as customer_name, c.email as customer_email, c.phone as customer_phone
                    FROM rentals r
                    LEFT JOIN vehicles v ON r.vehicle_id = v.id
                    LEFT JOIN customers c ON r.customer_id = c.id
                    WHERE r.id = ?;
                """, (rental_id,))
                row = cursor.fetchone()
                conn.close()
                return [dict(row)] if row else f"⚠️ Rental ID {rental_id} not found."
            except Exception as e:
                return f"❌ SQLite Error while searching rental: {e}"
        else:
            try:
                result = (
                    self.client.table("rentals")
                    .select("*, vehicles(*), customers(*)")
                    .eq("id", rental_id)
                    .execute()
                    .data
                )
                if result:
                    r = result[0]
                    flat_r = r.copy()
                    if "vehicles" in r and isinstance(r["vehicles"], dict):
                        flat_r["vehicle_plate"] = r["vehicles"].get("plate")
                        flat_r["vehicle_model"] = r["vehicles"].get("model")
                        flat_r["vehicle_rate"] = r["vehicles"].get("rate")
                    if "customers" in r and isinstance(r["customers"], dict):
                        flat_r["customer_name"] = r["customers"].get("name")
                        flat_r["customer_email"] = r["customers"].get("email")
                        flat_r["customer_phone"] = r["customers"].get("phone")
                    return [flat_r]
                return f"⚠️ Rental ID {rental_id} not found."
            except APIError as e:
                return f"❌ Database error while searching rental: {e}"
