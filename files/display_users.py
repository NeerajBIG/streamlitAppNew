import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
import mysql.connector

def fetch_users_with_status():
    db = mysql.connector.connect(
        host='sql5.freesqldatabase.com',
        user='sql5801118',
        password='mqgWHRyzR1',
        database='sql5801118'
    )
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT userid, SessionActive, SessionTime FROM SessionDetails")
    sessions = cursor.fetchall()
    user_status = {}
    for session in sessions:
        user_id, session_active, session_time = session
        if session_active == 1:
            user_status[user_id] = {"status": "Active", "last_active": None}
        else:
            user_status[user_id] = {"status": f"Last active on {session_time}", "last_active": session_time}

    user_data = []
    for user in users:
        user_id, name = user
        status = user_status.get(user_id, {"status": "Unknown", "last_active": None})

        initials = ''.join([part[0].upper() for part in name.split() if part])  # Extract initials
        status_str = str(status["status"])  # Explicitly cast to string to avoid type mismatch
        name_str = str(name)
        user_data.append((user_id, name_str, initials, status_str))  # Ensure it's a tuple

    cursor.close()
    db.close()

    return user_data
