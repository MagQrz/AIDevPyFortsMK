import math
from ping3 import ping

class Ping:
    # Ping-funktion
    def ping_host(self, ip, location):
        latency = ping(ip, timeout=2)  # 2-sekunder timeout för bättre resultat

        num = latency * 1000  # Float
        num_str = str(num)  # Convert to string

        truncated_str = num_str[:num_str.find('.') + 3]  # Keep only 2 decimals
        truncated_num = float(truncated_str)  # Convert back to float

        latency = truncated_num  # Float again

        if latency is not None:
            return {"ip": ip, "location": location, "latency_ms": latency, "status": "success"}
        else:
            return {"ip": ip, "location": location, "latency_ms": None, "status": "failure"}
