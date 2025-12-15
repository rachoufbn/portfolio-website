import sqlite3

class DatabaseService:
    """Database service with per-request connections."""

    def __init__(self, db_path):
        """Create a new connection for this request."""

        self.connection = sqlite3.connect(db_path, timeout=10.0)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute('PRAGMA foreign_keys = ON')
    
    def fetchAll(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        return [dict(row) for row in cursor.fetchall()]

    def fetchOne(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        row = cursor.fetchone()
        return dict(row) if row else None

    def insert(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        self.connection.commit()
        return cursor.lastrowid
        
    def execute(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        self.connection.commit()
        return cursor.rowcount
        
    def destroy(self):
        """Close the connection."""
        if self.connection:
            self.connection.close()
            self.connection = None