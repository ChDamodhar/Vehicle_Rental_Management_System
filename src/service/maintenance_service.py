from src.dao.maintenance_dao import MaintenanceDAO

class MaintenanceService:
    def __init__(self):
        self.dao = MaintenanceDAO()

    def add_maintenance(self, vehicle_id, description, cost, date):
        return self.dao.add_maintenance(vehicle_id, description, cost, date)

    def update_maintenance(self, maintenance_id, description=None, cost=None, date=None):
        return self.dao.update_maintenance(maintenance_id, description, cost, date)

    def delete_maintenance(self, maintenance_id):
        return self.dao.delete_maintenance(maintenance_id)

    def list_maintenance(self):
        return self.dao.list_maintenance()

    def search_maintenance(self, maintenance_id):
        return self.dao.search_maintenance(maintenance_id)
