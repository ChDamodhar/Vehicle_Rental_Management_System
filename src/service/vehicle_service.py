from src.dao.vehicle_dao import VehicleDAO

class VehicleService:
    def __init__(self):
        self.dao = VehicleDAO()

    def add_vehicle(self, plate, model, vtype, rate):
        return self.dao.add_vehicle(plate, model, vtype, rate)

    def update_vehicle(self, vehicle_id, model=None, vtype=None, rate=None, available=None):
        return self.dao.update_vehicle(vehicle_id, model, vtype, rate, available)

    def delete_vehicle(self, vehicle_id):
        return self.dao.delete_vehicle(vehicle_id)

    def list_vehicles(self):
        return self.dao.list_vehicles()

    def search_vehicle(self, keyword):
        return self.dao.search_vehicle(keyword)
