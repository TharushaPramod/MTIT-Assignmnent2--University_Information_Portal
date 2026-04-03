from data_service import EventMongoDataService 
class EventService:
    def __init__(self):
        self.data_service = EventMongoDataService() 
    def get_all(self):
        return self.data_service.get_all_events()
    
    def get_by_id(self, event_id: str):
        return self.data_service.get_event_by_id(event_id)
    
    def create(self, event_data):
        return self.data_service.add_event(event_data)
    
    def update(self, event_id: str, event_data): 
        return self.data_service.update_event(event_id, event_data)
    
    def delete(self, event_id: str): 
        return self.data_service.delete_event(event_id)