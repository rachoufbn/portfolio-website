from .database import DatabaseService
from .meetings import MeetingsService

class ChatHistoryService:

    def __init__(self, db: DatabaseService, meeting_id: int, user_id: int):

        self.db = db
        self.meeting_id = meeting_id

        meetings_service = MeetingsService(self.db, user_id)
        if not meetings_service.user_has_meeting(meeting_id):
            raise RuntimeError("Permission error: user does not own this meeting")
        
    # Fetch full chat history
    def get(self):
        query = "SELECT * FROM chat_history WHERE meeting_id = ?;"
        return self.db.fetchAll(query, (self.meeting_id,))

    # Insert chat history item
    def insert(self, role, content, notes_version):
        query = """
            INSERT INTO chat_history (meeting_id, role, content, notes_version)
            VALUES (?, ?, ?, ?)
        """
        chat_history_id = self.db.insert(query, (self.meeting_id, role, content, notes_version))
        return chat_history_id

    # Delete chat history back to (and including) specified id
    def delete(self, chat_history_id):
        query = """
            DELETE FROM chat_history
            WHERE id >= ?
              AND meeting_id = ?
        """
        affected_row_count = self.db.execute(query, (chat_history_id, self.meeting_id))
        return affected_row_count