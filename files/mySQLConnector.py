import mysql.connector
from mysql.connector import Error


class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    # Establishing connection
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if self.connection.is_connected():
                print(f"Connected to {self.database} database")
            else:
                print("Failed to connect to database")
        except Error as e:
            print(f"Error: {e}")

    # Closing connection
    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Connection closed.")

    # Execute select query and return results
    def execute_query(self, query, params=None):
        if not self.connection:
            print("No active connection. Please connect to the database first.")
            return

        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Error: {e}")
            return None

    # Execute insert, update, delete query (for non-select queries)
    def execute_update(self, query, params=None):
        if not self.connection:
            print("No active connection. Please connect to the database first.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            return f"Query executed successfully. {cursor.rowcount} row(s) affected."

        except Error as e:
            self.connection.rollback()
            return f"Error: {e}"

    def fetch_data(self, query, params=None):
        return self.execute_query(query, params)

    def insert_data(self, query, params=None):
        self.execute_update(query, params)

    def update_data(self, query, params=None):
        self.execute_update(query, params)

    def delete_data(self, query, params=None):
        self.execute_update(query, params)