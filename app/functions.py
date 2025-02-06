import sqlite3
import math
from ping3 import ping
from config import Config


def just_one_pdbpost():
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT location FROM ping_data_compare WHERE id = ?", (99,))
    data = cursor.fetchone()  # Fetch a single post from row

    conn.close()
    return data

def one_ping():
        ip = "103.253.133.80"
        latency = ping(ip, timeout=2)  # 2-sekunder timeout för bättre resultat
        
        num = latency * 1000  # Float
        num_str = str(num)  # Convert to string

        truncated_str = num_str[:num_str.find('.') + 3]  # Keep only 2 decimals
        truncated_num = float(truncated_str)  # Convert back to float

        latency = truncated_num  # Float again

        if latency is not None:
            print(latency)
            return {"ip": ip, "location": "Bangkok", "latency_ms": latency, "status": "success"}
        else:
            return {"ip": ip, "location": "Bangkok", "latency_ms": None, "status": "failure"}
