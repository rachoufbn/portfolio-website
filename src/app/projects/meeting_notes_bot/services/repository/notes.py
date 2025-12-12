from .database import DatabaseService
from .meetings import MeetingsService

class NotesService:

    def __init__(self, db: DatabaseService, meeting_id: int, user_id: int):

        self.db = db
        self.meeting_id = meeting_id

        meetings_service = MeetingsService(self.db, user_id)
        if not meetings_service.user_has_meeting(meeting_id):
            raise RuntimeError("Permission error: user does not own this meeting")
        
    # Create a new notes version
    def create(self, notes: str):
        query = """
            INSERT INTO notes (meeting_id, version, notes)
            SELECT
                %s,
                COALESCE(MAX(version) + 1, 1) AS next_version,
                %s
            FROM notes
            WHERE meeting_id = %s
        """
        self.db.insert(query, (self.meeting_id, notes, self.meeting_id))

    # Get the latest notes version unless specified
    def get(self, version: int = None):
        if(version):
            query = """
                SELECT * FROM notes
                WHERE meeting_id = %s
                  AND version = %s
            """
            return self.db.fetchOne(query, (self.meeting_id, version))
        else:
            query = """
                SELECT * FROM notes
                WHERE meeting_id = %s
                ORDER BY n.version DESC
                LIMIT 1
            """
            return self.db.fetchOne(query, (self.meeting_id))
    