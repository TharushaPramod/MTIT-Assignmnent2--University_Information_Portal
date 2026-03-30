from data_service import StaffMongoDataService

class StaffService:
    def __init__(self):
        self.data_service = StaffMongoDataService()

    def get_all(self):
        return self.data_service.get_all_staff()

    def get_by_id(self, staff_id: str):
        return self.data_service.get_staff_by_id(staff_id)

    def create(self, staff_data):
        return self.data_service.add_staff(staff_data)

    def update(self, staff_id: str, staff_data):
        return self.data_service.update_staff(staff_id, staff_data)

    def delete(self, staff_id: str):
        return self.data_service.delete_staff(staff_id)
