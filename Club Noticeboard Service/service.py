from data_service import NoticeMongoDataService

class NoticeService:
    def __init__(self):
        self.data_service = NoticeMongoDataService()

    def get_all(self):
        return self.data_service.get_all_notices()

    def get_by_id(self, notice_id: str):
        return self.data_service.get_notice_by_id(notice_id)

    def create(self, notice_data):
        return self.data_service.add_notice(notice_data)

    def update(self, notice_id: str, notice_data):
        return self.data_service.update_notice(notice_id, notice_data)

    def delete(self, notice_id: str):
        return self.data_service.delete_notice(notice_id)