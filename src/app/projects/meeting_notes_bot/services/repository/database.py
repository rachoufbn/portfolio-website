from dbutils.pooled_db import PooledDB
import pymysql
from pymysql.cursors import DictCursor

class DatabaseService:
    """Database service with connection pooling."""

    _pool = None
    
    @classmethod
    def initialize_pool(cls, host, port, user, password, database, 
                       min_connections=1, max_connections=10):
        """Initialize the connection pool at app startup."""
        if cls._pool is None:
            cls._pool = PooledDB(
                creator=pymysql,
                mincached=min_connections,
                maxcached=max_connections,
                maxconnections=max_connections,
                blocking=True,  # Wait if no connections available
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                charset='utf8mb4',
                cursorclass=DictCursor
            )


    def __init__(self):
        """Get a connection from the pool."""

        if self._pool is None:
            raise RuntimeError("Pool not initialized. Call initialize_pool() first.")
        
        self.connection = self._pool.connection()
    
    def fetchAll(self, query, params=None):
        
        with self.connection.cursor() as cursor:                
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def fetchOne(self, query, params=None):
        
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()

    def insert(self, query, params=None):
    
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor.lastrowid
        
    def execute(self, query, params=None):
    
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor.rowcount
        
    def destroy(self):
        """Returns connection to pool (doesn't actually close it)."""

        if self.connection:
            self.connection.close() # Returns to pool
            self.connection = None