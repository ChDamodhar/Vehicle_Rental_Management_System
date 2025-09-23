from src.db_config import get_supabase
from postgrest.exceptions import APIError

class MaintenanceDAO:
    def __init__(self):
        self.client = get_supabase()

    def add_maintenance(self, vehicle_id, description, cost, date):
        try:
            result = self.client.table("maintenance").insert({
                "vehicle_id": vehicle_id,
                "description": description,
                "cost": cost,
                "date": date
            }).execute().data
            return f"Maintenance added: {result}"
        except APIError as e:
            return f"Database error while adding maintenance: {e}"

    def update_maintenance(self, maintenance_id, description=None, cost=None, date=None):
        try:
            update_data = {}
            if description: update_data["description"] = description
            if cost: update_data["cost"] = cost
            if date: update_data["date"] = date

            result = self.client.table("maintenance").update(update_data).eq("id", maintenance_id).execute().data
            if result:
                return f"Maintenance updated: {result}"
            return f"Maintenance ID {maintenance_id} not found."
        except APIError as e:
            return f"Database error while updating maintenance: {e}"

    def delete_maintenance(self, maintenance_id):
        try:
            result = self.client.table("maintenance").delete().eq("id", maintenance_id).execute().data
            if result:
                return f"Maintenance {maintenance_id} deleted."
            return f"Maintenance ID {maintenance_id} not found."
        except APIError as e:
            return f"Database error while deleting maintenance: {e}"

    def list_maintenance(self):
        try:
            return self.client.table("maintenance").select("*").execute().data
        except APIError as e:
            return f"Database error while fetching maintenance records: {e}"

    def search_maintenance(self, maintenance_id):
        try:
            result = self.client.table("maintenance").select("*").eq("id", maintenance_id).execute().data
            return result if result else f"Maintenance ID {maintenance_id} not found."
        except APIError as e:
            return f"Database error while searching maintenance: {e}"
