import sqlite3

from config import Config


def just_one_pdbpost():
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT location FROM ping_data_compare WHERE id = ?", (99,))
    data = cursor.fetchone()  # Fetch a single post from row

    conn.close()
    return data

# Call the function and print the result
post = just_one_pdbpost()
print(post)