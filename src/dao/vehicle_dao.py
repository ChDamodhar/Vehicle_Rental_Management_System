from src.db_config import get_supabase, get_db_mode, get_sqlite_conn
from postgrest.exceptions import APIError
import sqlite3

class VehicleDAO:
    def __init__(self):
        self.mode = get_db_mode()
        if self.mode == "supabase":
            self.client = get_supabase()

    def add_vehicle(self, plate, model, vtype, rate, available=True):
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO vehicles (plate, model, type, rate, available)
                    VALUES (?, ?, ?, ?, ?);
                """, (plate, model, vtype, rate, 1 if available else 0))
                conn.commit()
                row_id = cursor.lastrowid
                conn.close()
                return f"✅ Vehicle added successfully in SQLite. ID: {row_id}"
            except sqlite3.IntegrityError as e:
                return f"❌ Plate '{plate}' already exists: {e}"
            except Exception as e:
                return f"❌ SQLite Error while adding vehicle: {e}"
        else:
            try:
                result = self.client.table("vehicles").insert({
                    "plate": plate,
                    "model": model,
                    "type": vtype,
                    "rate": rate,
                    "available": available
                }).execute().data
                return f"✅ Vehicle added successfully: {result}"
            except APIError as e:
                return f"❌ Database error while adding vehicle: {e}"

    def update_vehicle(self, vehicle_id, model=None, vtype=None, rate=None, available=None):
        if self.mode == "sqlite":
            try:
                update_data = []
                query_parts = []
                if model is not None:
                    query_parts.append("model = ?")
                    update_data.append(model)
                if vtype is not None:
                    query_parts.append("type = ?")
                    update_data.append(vtype)
                if rate is not None:
                    query_parts.append("rate = ?")
                    update_data.append(rate)
                if available is not None:
                    query_parts.append("available = ?")
                    update_data.append(1 if available else 0)

                if not query_parts:
                    return "⚠️ No fields provided to update."

                update_data.append(vehicle_id)
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute(f"""
                    UPDATE vehicles
                    SET {", ".join(query_parts)}
                    WHERE id = ?;
                """, tuple(update_data))
                conn.commit()
                changes = conn.total_changes
                conn.close()

                if changes > 0:
                    return f"✅ Vehicle ID {vehicle_id} updated successfully in SQLite."
                return f"⚠️ Vehicle ID {vehicle_id} not found."
            except Exception as e:
                return f"❌ SQLite Error while updating vehicle: {e}"
        else:
            try:
                update_data = {}
                if model is not None: update_data["model"] = model
                if vtype is not None: update_data["type"] = vtype
                if rate is not None: update_data["rate"] = rate
                if available is not None: update_data["available"] = available

                if not update_data:
                    return "⚠️ No fields provided to update."

                result = self.client.table("vehicles").update(update_data).eq("id", vehicle_id).execute().data
                if result:
                    return f"✅ Vehicle updated successfully: {result}"
                return f"⚠️ Vehicle ID {vehicle_id} not found."
            except APIError as e:
                return f"❌ Database error while updating vehicle: {e}"

    def delete_vehicle(self, vehicle_id):
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM vehicles WHERE id = ?;", (vehicle_id,))
                conn.commit()
                changes = conn.total_changes
                conn.close()
                if changes > 0:
                    return f"🗑️ Vehicle {vehicle_id} deleted successfully from SQLite."
                return f"⚠️ Vehicle ID {vehicle_id} not found."
            except Exception as e:
                return f"❌ SQLite Error while deleting vehicle: {e}"
        else:
            try:
                result = self.client.table("vehicles").delete().eq("id", vehicle_id).execute().data
                if result:
                    return f"🗑️ Vehicle {vehicle_id} deleted successfully."
                return f"⚠️ Vehicle ID {vehicle_id} not found."
            except APIError as e:
                return f"❌ Database error while deleting vehicle: {e}"

    def list_vehicles(self):
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM vehicles ORDER BY id DESC;")
                rows = cursor.fetchall()
                conn.close()
                return [dict(r) for r in rows]
            except Exception as e:
                return f"❌ SQLite Error while fetching vehicles: {e}"
        else:
            try:
                result = self.client.table("vehicles").select("*").execute().data
                return result if result else []
            except APIError as e:
                return f"❌ Database error while fetching vehicles: {e}"

    def search_vehicle(self, keyword):
        """Searches vehicle by plate (wildcard) or exact ID if keyword is digits."""
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                if str(keyword).isdigit():
                    cursor.execute("SELECT * FROM vehicles WHERE id = ? OR plate LIKE ?;", (int(keyword), f"%{keyword}%"))
                else:
                    cursor.execute("SELECT * FROM vehicles WHERE plate LIKE ? OR model LIKE ?;", (f"%{keyword}%", f"%{keyword}%"))
                rows = cursor.fetchall()
                conn.close()
                return [dict(r) for r in rows] if rows else f"⚠️ No vehicles found matching: '{keyword}'"
            except Exception as e:
                return f"❌ SQLite Error while searching vehicles: {e}"
        else:
            try:
                # If keyword is numeric, try searching by ID as well
                if str(keyword).isdigit():
                    result = self.client.table("vehicles").select("*").eq("id", int(keyword)).execute().data
                    if result:
                        return result

                result = self.client.table("vehicles").select("*").ilike("plate", f"%{keyword}%").execute().data
                return result if result else f"⚠️ No vehicles found matching: '{keyword}'"
            except APIError as e:
                return f"❌ Database error while searching vehicle: {e}"

    def set_availability(self, vehicle_id, available):
        """Helper to quickly set a vehicle's availability status."""
        return self.update_vehicle(vehicle_id, available=available)
