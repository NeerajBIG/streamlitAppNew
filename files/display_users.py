import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
import mysql.connector

def fetch_sessions():
    db = mysql.connector.connect(
        host='sql5.freesqldatabase.com',
        user='sql5801118',
        password='mqgWHRyzR1',
        database='sql5801118'
    )

    cursor = db.cursor()

    query = "SELECT userid, SessionActive, SessionTime FROM SessionDetails"
    cursor.execute(query)

    sessions = cursor.fetchall()

    cursor.close()
    db.close()

    session_info = []
    for session in sessions:
        userid, session_active, session_time = session

        if session_active == 1:
            status = "Active"
        else:
            status = f"Last active on {session_time}"

        session_info.append((userid, status))

    return session_info
