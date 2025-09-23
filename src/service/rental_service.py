from src.dao.rental_dao import RentalDAO

class RentalService:
    def __init__(self):
        self.dao = RentalDAO()

    def create_rental(self, customer_id, vehicle_id, rental_date, return_date):
        return self.dao.create_rental(customer_id, vehicle_id, rental_date, return_date)

    def end_rental(self, rental_id, actual_return_date):
        return self.dao.end_rental(rental_id, actual_return_date)

    def delete_rental(self, rental_id):
        return self.dao.delete_rental(rental_id)

    def list_rentals(self):
        return self.dao.list_rentals()

    def search_rentals(self, keyword):
        return self.dao.search_rentals(keyword)
