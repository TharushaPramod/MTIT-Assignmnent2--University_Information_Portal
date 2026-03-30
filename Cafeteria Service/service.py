from data_service import CafeteriaMongoDataService

class CafeteriaService:
    def __init__(self):
        self.data_service = CafeteriaMongoDataService()

    def get_all(self):
        return self.data_service.get_all_menu_items()

    def get_by_id(self, item_id: str):
        return self.data_service.get_menu_item_by_id(item_id)

    def create(self, menu_data):
        return self.data_service.add_menu_item(menu_data)

    def update(self, item_id: str, menu_data):
        return self.data_service.update_menu_item(item_id, menu_data)

    def delete(self, item_id: str):
        return self.data_service.delete_menu_item(item_id)