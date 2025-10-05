from files.mySQLConnector import MySQLDatabase


def main():
    # Creating database instance
    db = MySQLDatabase(
        host='sql5.freesqldatabase.com',
        user='sql5801118',
        password='mqgWHRyzR1',
        database='sql5801118'
    )
    db.connect()

    create_table_query = "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL, age INT NOT NULL, email VARCHAR(255) UNIQUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
    db.execute_update(create_table_query)

    # Example SELECT query (fetching data)
    select_query = "SELECT * FROM users WHERE age = %s"
    params = ('12',)
    result = db.fetch_data(select_query, params)
    print("SELECT Query Result:", result)

    # # Example INSERT query (inserting data)
    # insert_query = "INSERT INTO users (name, age, email) VALUES (%s, %s, %s)"
    # insert_params = ('xyz', '123', 'a1@a.com')
    # db.insert_data(insert_query, insert_params)

    # # Example UPDATE query (updating data)
    # update_query = "UPDATE users SET column1 = %s WHERE column2 = %s"
    # update_params = ('new_value', 'value2')
    # db.update_data(update_query, update_params)
    #
    # # Example DELETE query (deleting data)
    # delete_query = "DELETE FROM users WHERE column_name = %s"
    # delete_params = ('some_value',)
    # db.delete_data(delete_query, delete_params)

    db.close()

if __name__ == '__main__':
    main()