from datetime import datetime
from app.db import Database
from app.ping import Ping
from config import Config
from slask.flask_app import FlaskApp
import sqlite3


class App:

    def __init__(self):
        
        self.ping = Ping()
        self.db = Database()
        self.config = Config()

    def run(self):
        conn = sqlite3.connect(Config.DB_PATH)   
        #self.db.setup_database() Run one time only
    
        # Lista på IPs Asien(lokalt), Sverige och USA
        ip_list = [
            ("103.253.133.80", "Bangkok"),
            ("90.130.70.73", "Stockholm"),
            ("208.67.222.222", "USA")
        ]

        # Pingar varje IP och sparar resultaten i databasen
        for ip, location in ip_list:
            result = self.ping.ping_host(ip, location)
            self.db.store_result(conn, result)
            # Get current time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Pinged {ip} ({location}): {result['latency_ms']} ms - {result['status']}")

        conn.close()
