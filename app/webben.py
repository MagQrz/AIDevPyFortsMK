import sqlite3
from flask import Flask, render_template, jsonify
import pandas as pd

DB_PATH = "/Users/magnuskurtz/2024/Programmering/Prog1Code/2025MagKurPythFortsExam/db_storage/ping_results.db"

app = Flask(__name__)

def get_data():
    conn = sqlite3.connect(DB_PATH)        
    query = "SELECT location, DATETIME(timestamp, '+7 hours') AS timestamp_bkk, latency_ms FROM ping_data_compare ORDER BY location, timestamp_bkk DESC"
    df = pd.read_sql_query(query, conn) # row above convert timestamp from UTC to Bangkok time
    conn.close()

    # Konvertera timestamp till datetime
    df['timestamp_bkk'] = pd.to_datetime(df['timestamp_bkk'])
    #df = df.sort_values(by='timestamp_bkk')  # Sort by time
    df = df.sort_values(by=['location', 'timestamp_bkk'])  # Sort by location and time

    return df

@app.route("/")
def indexgraf():
    return render_template("indexgraf.html")

@app.route("/data")
def data():
    df = get_data()
    
    if df.empty:
        print("Error: No data in the database")
        return jsonify({"error": "No data available"}), 500  

    # Sort by location first, then timestamp
    df = df.sort_values(by=['location', 'timestamp_bkk'])

    # Create unique timestamp list för x-axis
    all_timestamps = sorted(df["timestamp_bkk"].dt.strftime('%Y-%m-%d %H:%M:%S').unique())

    # Group data by location
    grouped = df.groupby("location")
    data = {"timestamps": all_timestamps}  # Shared X-axis timestamps

    # Secure every location's data match shared timestamps
    for location, group in grouped:
        latency_dict = dict(zip(group["timestamp_bkk"].dt.strftime('%Y-%m-%d %H:%M:%S'), group["latency_ms"]))        
        # Fill missing timestamps with None (ensures data aligns correctly)
        latency_list = [latency_dict.get(ts, None) for ts in all_timestamps]

        data[location] = {
            "timestamps": all_timestamps, 
            "latency": latency_list
        }

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)