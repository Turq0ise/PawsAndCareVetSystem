import sqlite3
import datetime
from modules.idGen import idGen

class ClinicDatabase:
    _instance = None

    def __new__(cls, db_name="clinic.db"):
        if cls._instance is None:
            cls._instance = super(ClinicDatabase, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_name="clinic.db"):
        if getattr(self, "_initialized", False):
            return

        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row
        
        self.connection.execute("PRAGMA foreign_keys = ON;")
        
        self._create_tables()
        self._initialized = True

    def _create_tables(self):
        """Creates the required tables if they do not already exist."""
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS owners (
                owner_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                contact_number TEXT NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                pet_id TEXT PRIMARY KEY,
                owner_id TEXT NOT NULL,
                name TEXT NOT NULL,
                species TEXT NOT NULL CHECK(species IN ('Dog', 'Cat', 'Bird', 'Rabbit')),
                age INTEGER,
            
                FOREIGN KEY (owner_id) REFERENCES owners(owner_id) ON DELETE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id TEXT PRIMARY KEY,
                pet_id TEXT NOT NULL,
                reason TEXT,
                date DATE,
                time TIME,
                status TEXT DEFAULT 'Scheduled' CHECK(status IN ('Scheduled', 'Completed', 'Cancelled')),

                FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE
            );
        """)

        self.connection.commit()

    def execute_query(self, query: str, params: tuple = ()):
        """Executes an INSERT, UPDATE, or DELETE query and commits changes."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
        except sqlite3.Error:
            self.connection.rollback()
            raise
        return cursor

    def fetch_all(self, query: str, params: tuple = ()):
        """Executes a SELECT query and returns all matching rows."""
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def fetch_one(self, query: str, params: tuple = ()):
        """Executes a SELECT query and returns a single matching row."""
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    def close(self):
        """Closes the active database connection."""
        if self.connection:
            self.connection.close()

    @classmethod
    def reset_instance(cls):
        """Helper to clear singleton state - useful between unit tests."""
        if cls._instance:
            cls._instance.close()
        cls._instance = None
