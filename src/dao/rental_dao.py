from src.db_config import get_supabase
from postgrest.exceptions import APIError


class RentalDAO:
    def __init__(self):
        self.client = get_supabase()

    def add_rental(self, vehicle_id, customer_id, start_date, end_date):
        """
        Add a new rental record to the database.
        """
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
            return f"✅ Rental added successfully: {result}"
        except APIError as e:
            return f"❌ Database error while adding rental: {e}"

    def update_rental(self, rental_id, start_date=None, end_date=None):
        """
        Update rental dates.
        """
        try:
            update_data = {}
            if start_date:
                update_data["start_date"] = start_date
            if end_date:
                update_data["end_date"] = end_date

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
        """
        Delete a rental record by ID.
        """
        try:
            result = (
                self.client.table("rentals")
                .delete()
                .eq("id", rental_id)
                .execute()
                .data
            )
            if result:
                return f"🗑️ Rental {rental_id} deleted successfully."
            return f"⚠️ Rental ID {rental_id} not found."
        except APIError as e:
            return f"❌ Database error while deleting rental: {e}"

    def list_rentals(self):
        """
        Retrieve all rentals.
        """
        try:
            result = self.client.table("rentals").select("*").execute().data
            return result
        except APIError as e:
            return f"❌ Database error while fetching rentals: {e}"

    def search_rental(self, rental_id):
        """
        Search rental by ID.
        """
        try:
            result = (
                self.client.table("rentals")
                .select("*")
                .eq("id", rental_id)
                .execute()
                .data
            )
            return result if result else f"⚠️ Rental ID {rental_id} not found."
        except APIError as e:
            return f"❌ Database error while searching rental: {e}"
