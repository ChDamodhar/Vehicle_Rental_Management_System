from src.dao.maintenance_dao import MaintenanceDAO

class MaintenanceService:
    def __init__(self):
        self.dao = MaintenanceDAO()

    def add_maintenance(self, vehicle_id, description, maintenance_date, status):
        return self.dao.add_maintenance(vehicle_id, description, maintenance_date, status)

    def update_maintenance(self, maintenance_id, description=None, maintenance_date=None, status=None):
        fields = {k: v for k, v in {
            "description": description,
            "maintenance_date": maintenance_date,
            "status": status
        }.items() if v is not None}
        return self.dao.update_maintenance(maintenance_id, fields)

    def delete_maintenance(self, maintenance_id):
        return self.dao.delete_maintenance(maintenance_id)

    def list_maintenance(self):
        return self.dao.list_maintenance()

    def search_maintenance(self, keyword):
        return self.dao.search_maintenance(keyword)
