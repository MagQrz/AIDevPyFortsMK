import sqlite3
from flask import Flask, render_template, jsonify
import pandas as pd

server = Flask(__name__)

@server.route("/")
def indexgraf():
    return render_template("indexgraf.html")

@server.route("/data")
def data():
    conn = sqlite3.connect("ping_results.db")  # Connect to SQLite
    query = "SELECT location, DATETIME(timestamp, '+7 hours') AS timestamp_bkk, latency_ms FROM ping_data_compare ORDER BY location, timestamp_bkk DESC LIMIT 100"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convert timestamp to datetime
    df['timestamp_bkk'] = pd.to_datetime(df['timestamp_bkk'])
    #df = df.sort_values(by='timestamp_bkk')  # Sort by time
    df = df.sort_values(by=['location', 'timestamp_bkk'])  # Sort by location and time
    print(df)
    
    if df.empty:
        print("Error: No data in the database")
        return jsonify({"error": "No data available"}), 500  

    # ✅ Sort by location first, then by timestamp
    df = df.sort_values(by=['location', 'timestamp_bkk'])

    # ✅ Create a shared, unique timestamp list for the x-axis
    all_timestamps = sorted(df["timestamp_bkk"].dt.strftime('%Y-%m-%d %H:%M:%S').unique())

    # ✅ Group data by location
    grouped = df.groupby("location")
    data = {"timestamps": all_timestamps}  # Shared X-axis timestamps

    # ✅ Ensure each location's data matches the shared timestamps
    for location, group in grouped:
        latency_dict = dict(zip(group["timestamp_bkk"].dt.strftime('%Y-%m-%d %H:%M:%S'), group["latency_ms"]))        
        # Fill missing timestamps with None (ensures data aligns correctly)
        latency_list = [latency_dict.get(ts, None) for ts in all_timestamps]

        data[location] = {
            "timestamps": all_timestamps,  # Keep timestamps consistent
            "latency": latency_list
        }

    print("Sending Data:", data)  # Debugging
    return jsonify(data)

def run(debug=False):
    server.run(debug=debug)  # Change to port 8080

if __name__ == '__main__':
    server.run(debug=True)