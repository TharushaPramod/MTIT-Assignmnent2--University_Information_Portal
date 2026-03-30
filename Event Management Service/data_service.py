from models import Event

class EventMockDataService:
    def __init__(self):
        self.events = [
            Event(id=1, title="AI in Healthcare", description="A session on AI applications in medicine.", date="2026-04-10", time="10:00 AM", venue="Main Auditorium", event_type="Academic Workshop"),
            Event(id=2, title="Tech Career Fair", description="Annual university career fair for IT students.", date="2026-04-15", time="09:00 AM", venue="Campus Grounds", event_type="Campus Event"),
            Event(id=3, title="Guest Lecture: Quantum Computing", description="An introduction to quantum computing by Dr. Smith.", date="2026-04-20", time="02:00 PM", venue="Lecture Hall A", event_type="Guest Lecture"),
        ]
        self.next_id = 4
    
    def get_all_events(self):
        return self.events
    
    def get_event_by_id(self, event_id: int):
        return next((e for e in self.events if e.id == event_id), None)
    
    def add_event(self, event_data):
        new_event = Event(id=self.next_id, **event_data.model_dump())
        self.events.append(new_event)
        self.next_id += 1
        return new_event
    
    def update_event(self, event_id: int, event_data):
        event = self.get_event_by_id(event_id)
        if event:
            update_data = event_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(event, key, value)
            return event
        return None
    
    def delete_event(self, event_id: int):
        event = self.get_event_by_id(event_id)
        if event:
            self.events.remove(event)
            return True
        return False
