from src.db_config import get_supabase
from postgrest.exceptions import APIError

class VehicleDAO:
    def __init__(self):
        self.client = get_supabase()

    def add_vehicle(self, model, type, rate, available=True):
        try:
            result = self.client.table("vehicles").insert({
                "model": model,
                "type": type,
                "rate": rate,
                "available": available
            }).execute().data
            return f"Vehicle added: {result}"
        except APIError as e:
            return f"Database error while adding vehicle: {e}"

    def update_vehicle(self, vehicle_id, model=None, type=None, rate=None, available=None):
        try:
            update_data = {}
            if model: update_data["model"] = model
            if type: update_data["type"] = type
            if rate: update_data["rate"] = rate
            if available is not None: update_data["available"] = available

            result = self.client.table("vehicles").update(update_data).eq("id", vehicle_id).execute().data
            if result:
                return f"Vehicle updated: {result}"
            return f"Vehicle ID {vehicle_id} not found."
        except APIError as e:
            return f"Database error while updating vehicle: {e}"

    def delete_vehicle(self, vehicle_id):
        try:
            result = self.client.table("vehicles").delete().eq("id", vehicle_id).execute().data
            if result:
                return f"Vehicle {vehicle_id} deleted."
            return f"Vehicle ID {vehicle_id} not found."
        except APIError as e:
            return f"Database error while deleting vehicle: {e}"

    def list_vehicles(self):
        try:
            return self.client.table("vehicles").select("*").execute().data
        except APIError as e:
            return f"Database error while fetching vehicles: {e}"

    def search_vehicle(self, vehicle_id):
        try:
            result = self.client.table("vehicles").select("*").eq("id", vehicle_id).execute().data
            return result if result else f"Vehicle ID {vehicle_id} not found."
        except APIError as e:
            return f"Database error while searching vehicle: {e}"
