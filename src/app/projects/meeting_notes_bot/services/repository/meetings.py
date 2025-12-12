from .database import DatabaseService

class MeetingsService:

    def __init__(self, db: DatabaseService, user_id: int):
        self.db = db
        self.user_id = user_id

    def create(self, title: str, timestamp, transcript: str):
        query = """
            INSERT INTO meetings (title, timestamp, transcript, user_id)
            VALUES (%s, %s, %s, %s);
        """
        meeting_id = self.db.insert(query, (title, timestamp, transcript, self.user_id))
        return meeting_id
    
    def update(self, meeting_id: int, title: str, timestamp):
        query = """
            UPDATE meetings
            SET title = %s, timestamp = %s
            WHERE id = %s AND user_id = %s;
        """
        affected_row_count = self.db.execute(query, (title, timestamp, meeting_id, self.user_id))
        return affected_row_count
    
    def delete(self, meeting_id: int):
        query = "DELETE FROM meetings WHERE id = %s AND user_id = %s;"
        affected_row_count = self.db.execute(query, (meeting_id, self.user_id))
        return affected_row_count
    
    def get(self, meeting_id: int = None):
        if(meeting_id):
            query = "SELECT * FROM meetings WHERE id = %s AND user_id = %s;"
            return self.db.fetchOne(query, (meeting_id, self.user_id))
        else:
            query = "SELECT * FROM meetings WHERE user_id = %s;"
            return self.db.fetchAll(query, (self.user_id))
    
    def user_has_meeting(self, meeting_id: int):

        if not meeting_id:
            return False

        return bool(self.get(meeting_id))

