import sqlite3
import os
from config import Config

class Database:

    # Setup SQLite database
    def setup_database(self):
        conn = sqlite3.connect(Config.DB_PATH)        
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ping_data_compare (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT,
                location TEXT,
                latency_ms REAL,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        return conn

    # Save result in database
    def store_result(self, conn, data):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ping_data_compare (ip_address, location, latency_ms, status)
            VALUES (?, ?, ?, ?)
        """, (data["ip"], data["location"], data["latency_ms"], data["status"]))
        conn.commit()
