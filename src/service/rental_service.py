from src.dao.rental_dao import RentalDAO

class RentalService:
    def __init__(self):
        self.dao = RentalDAO()

    def add_rental(self, vehicle_id, customer_id, start_date, end_date):
        return self.dao.add_rental(vehicle_id, customer_id, start_date, end_date)

    def update_rental(self, rental_id, start_date=None, end_date=None):
        return self.dao.update_rental(rental_id, start_date, end_date)

    def delete_rental(self, rental_id):
        return self.dao.delete_rental(rental_id)

    def list_rentals(self):
        return self.dao.list_rentals()

    def search_rental(self, rental_id):
        return self.dao.search_rental(rental_id)
