from src.db_config import get_supabase, get_db_mode, get_sqlite_conn
from postgrest.exceptions import APIError
import sqlite3

class MaintenanceDAO:
    def __init__(self):
        self.mode = get_db_mode()
        if self.mode == "supabase":
            self.client = get_supabase()

    def add_maintenance(self, vehicle_id, description, cost, date):
        """Insert a maintenance record and mark the vehicle as unavailable."""
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                
                # Check if vehicle exists
                cursor.execute("SELECT id FROM vehicles WHERE id = ?;", (vehicle_id,))
                if not cursor.fetchone():
                    conn.close()
                    return f"❌ Error: Vehicle ID {vehicle_id} not found."

                # Insert maintenance record
                cursor.execute("""
                    INSERT INTO maintenance (vehicle_id, description, cost, date)
                    VALUES (?, ?, ?, ?);
                """, (vehicle_id, description, cost, date))
                maintenance_id = cursor.lastrowid
                
                # Mark vehicle as unavailable
                cursor.execute("UPDATE vehicles SET available = 0 WHERE id = ?;", (vehicle_id,))
                
                conn.commit()
                conn.close()
                return f"✅ Maintenance record added in SQLite. ID: {maintenance_id} (Vehicle marked Unavailable)"
            except Exception as e:
                return f"❌ SQLite Error while adding maintenance: {e}"
        else:
            try:
                result = self.client.table("maintenance").insert({
                    "vehicle_id": vehicle_id,
                    "description": description,
                    "cost": cost,
                    "date": date
                }).execute().data
                if result:
                    # Mark vehicle as unavailable
                    self.client.table("vehicles").update({"available": False}).eq("id", vehicle_id).execute()
                    return f"✅ Maintenance added: {result} (Vehicle marked Unavailable)"
                return "❌ Failed to insert maintenance record."
            except APIError as e:
                return f"❌ Database error while adding maintenance: {e}"

    def update_maintenance(self, maintenance_id, description=None, cost=None, date=None):
        if self.mode == "sqlite":
            try:
                update_data = []
                query_parts = []
                if description is not None:
                    query_parts.append("description = ?")
                    update_data.append(description)
                if cost is not None:
                    query_parts.append("cost = ?")
                    update_data.append(cost)
                if date is not None:
                    query_parts.append("date = ?")
                    update_data.append(date)

                if not query_parts:
                    return "⚠️ No fields provided to update."

                update_data.append(maintenance_id)
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute(f"""
                    UPDATE maintenance
                    SET {", ".join(query_parts)}
                    WHERE id = ?;
                """, tuple(update_data))
                conn.commit()
                changes = conn.total_changes
                conn.close()

                if changes > 0:
                    return f"✅ Maintenance ID {maintenance_id} updated successfully in SQLite."
                return f"⚠️ Maintenance ID {maintenance_id} not found."
            except Exception as e:
                return f"❌ SQLite Error while updating maintenance: {e}"
        else:
            try:
                update_data = {}
                if description is not None: update_data["description"] = description
                if cost is not None: update_data["cost"] = cost
                if date is not None: update_data["date"] = date

                if not update_data:
                    return "⚠️ No fields provided to update."

                result = self.client.table("maintenance").update(update_data).eq("id", maintenance_id).execute().data
                if result:
                    return f"✅ Maintenance updated: {result}"
                return f"⚠️ Maintenance ID {maintenance_id} not found."
            except APIError as e:
                return f"❌ Database error while updating maintenance: {e}"

    def delete_maintenance(self, maintenance_id):
        """Delete maintenance record and release the vehicle back to available."""
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                
                # Fetch vehicle_id before deleting
                cursor.execute("SELECT vehicle_id FROM maintenance WHERE id = ?;", (maintenance_id,))
                row = cursor.fetchone()
                if not row:
                    conn.close()
                    return f"⚠️ Maintenance ID {maintenance_id} not found."
                
                vehicle_id = row["vehicle_id"]
                
                # Delete maintenance record
                cursor.execute("DELETE FROM maintenance WHERE id = ?;", (maintenance_id,))
                
                # Set vehicle back to available
                cursor.execute("UPDATE vehicles SET available = 1 WHERE id = ?;", (vehicle_id,))
                
                conn.commit()
                conn.close()
                return f"🗑️ Maintenance {maintenance_id} deleted successfully. Vehicle {vehicle_id} is now available."
            except Exception as e:
                return f"❌ SQLite Error while deleting maintenance: {e}"
        else:
            try:
                # Find vehicle_id first
                m_data = self.client.table("maintenance").select("vehicle_id").eq("id", maintenance_id).execute().data
                if not m_data:
                    return f"⚠️ Maintenance ID {maintenance_id} not found."
                
                vehicle_id = m_data[0].get("vehicle_id")
                
                result = self.client.table("maintenance").delete().eq("id", maintenance_id).execute().data
                if result:
                    # Restore vehicle availability
                    self.client.table("vehicles").update({"available": True}).eq("id", vehicle_id).execute()
                    return f"🗑️ Maintenance record {maintenance_id} deleted. Vehicle {vehicle_id} marked available."
                return f"⚠️ Maintenance ID {maintenance_id} not found."
            except APIError as e:
                return f"❌ Database error while deleting maintenance: {e}"

    def list_maintenance(self):
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT m.id, m.vehicle_id, m.description, m.cost, m.date, m.created_at,
                           v.plate as vehicle_plate, v.model as vehicle_model
                    FROM maintenance m
                    LEFT JOIN vehicles v ON m.vehicle_id = v.id
                    ORDER BY m.id DESC;
                """)
                rows = cursor.fetchall()
                conn.close()
                return [dict(r) for r in rows]
            except Exception as e:
                return f"❌ SQLite Error while fetching maintenance records: {e}"
        else:
            try:
                result = self.client.table("maintenance").select("*, vehicles(*)").execute().data
                flat_results = []
                for m in (result if result else []):
                    flat_m = m.copy()
                    if "vehicles" in m and isinstance(m["vehicles"], dict):
                        flat_m["vehicle_plate"] = m["vehicles"].get("plate")
                        flat_m["vehicle_model"] = m["vehicles"].get("model")
                    flat_results.append(flat_m)
                return flat_results
            except APIError as e:
                return f"❌ Database error while fetching maintenance records: {e}"

    def search_maintenance(self, maintenance_id):
        if self.mode == "sqlite":
            try:
                conn = get_sqlite_conn()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT m.id, m.vehicle_id, m.description, m.cost, m.date, m.created_at,
                           v.plate as vehicle_plate, v.model as vehicle_model
                    FROM maintenance m
                    LEFT JOIN vehicles v ON m.vehicle_id = v.id
                    WHERE m.id = ?;
                """, (maintenance_id,))
                row = cursor.fetchone()
                conn.close()
                return [dict(row)] if row else f"⚠️ Maintenance ID {maintenance_id} not found."
            except Exception as e:
                return f"❌ SQLite Error while searching maintenance: {e}"
        else:
            try:
                result = (
                    self.client.table("maintenance")
                    .select("*, vehicles(*)")
                    .eq("id", maintenance_id)
                    .execute()
                    .data
                )
                if result:
                    m = result[0]
                    flat_m = m.copy()
                    if "vehicles" in m and isinstance(m["vehicles"], dict):
                        flat_m["vehicle_plate"] = m["vehicles"].get("plate")
                        flat_m["vehicle_model"] = m["vehicles"].get("model")
                    return [flat_m]
                return f"⚠️ Maintenance ID {maintenance_id} not found."
            except APIError as e:
                return f"❌ Database error while searching maintenance: {e}"
