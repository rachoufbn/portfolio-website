from .database import DatabaseService
import sqlite3
from ...exceptions import UserFacingError

class UsersService:
    def __init__(self, db: DatabaseService):
        self.db = db

    def create(self, name: str, email: str, password_hash:str, default_prompt: str):
        name = name.strip()
        email = email.strip().lower() # Normalize email to lowercase
        default_prompt = default_prompt.strip()
        query = """
            INSERT INTO users (name, email, password_hash, default_prompt)
            VALUES (?, ?, ?, ?);
        """
        try:
            user_id = self.db.insert(query, (name, email, password_hash, default_prompt))
            return user_id
        except sqlite3.IntegrityError as e:
            raise UserFacingError("Email already in use, try logging in instead.")
    
    def update(self, user_id: int, name: str, default_prompt: str):
        name = name.strip()
        default_prompt = default_prompt.strip()
        query = """
            UPDATE users
            SET name = ?, default_prompt = ? WHERE id = ?;
        """
        affected_row_count = self.db.execute(query, (name, default_prompt, user_id))
        return affected_row_count

    def get(self, user_id: int = None, user_email: str = None):
        if(user_id):
            query = "SELECT * FROM users WHERE id = ?;"
            return self.db.fetchOne(query, (user_id,))
        elif(user_email):
            user_email = user_email.strip().lower() # Normalize email to lowercase
            query = "SELECT * FROM users WHERE email = ?;"
            return self.db.fetchOne(query, (user_email,))
        else:
            query = "SELECT * FROM users;"
            return self.db.fetchAll(query)