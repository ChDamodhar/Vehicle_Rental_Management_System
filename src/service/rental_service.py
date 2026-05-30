from src.dao.rental_dao import RentalDAO
from datetime import datetime

class RentalService:
    def __init__(self):
        self.dao = RentalDAO()

    def add_rental(self, vehicle_id, customer_id, start_date, end_date):
        """Add a new rental with date validation."""
        if not vehicle_id:
            return "❌ Error: Vehicle ID is required."
        if not customer_id:
            return "❌ Error: Customer ID is required."
        if not start_date or not end_date:
            return "❌ Error: Start Date and End Date are required."

        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            if end_dt < start_dt:
                return "❌ Error: End Date cannot be before Start Date."
        except ValueError:
            return "❌ Error: Dates must be in YYYY-MM-DD format."

        return self.dao.add_rental(vehicle_id, customer_id, start_date, end_date)

    def update_rental(self, rental_id, start_date=None, end_date=None):
        """Update rental dates with range validation."""
        if not rental_id:
            return "❌ Error: Rental ID is required."

        if start_date and end_date:
            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                if end_dt < start_dt:
                    return "❌ Error: End Date cannot be before Start Date."
            except ValueError:
                return "❌ Error: Dates must be in YYYY-MM-DD format."

        return self.dao.update_rental(rental_id, start_date, end_date)

    def delete_rental(self, rental_id):
        if not rental_id:
            return "❌ Error: Rental ID is required."
        return self.dao.delete_rental(rental_id)

    def list_rentals(self):
        return self.dao.list_rentals()

    def search_rental(self, rental_id):
        if not rental_id:
            return "❌ Error: Rental ID is required."
        return self.dao.search_rental(rental_id)
