from files.mySQLConnector import MySQLDatabase


db = MySQLDatabase(
        host='sql5.freesqldatabase.com',
        user='sql5801118',
        password='mqgWHRyzR1',
        database='sql5801118'
)
db.connect()

def show_usersAdmin1(userinsession):
    if userinsession == "Admin":
        st.text("Show table of all users here.")
    else:
        st.write("You need to log in first!")

# SELECT query (fetching data)
select_query = "SELECT * FROM users WHERE email = %s"
params = (email,)
result = db.fetch_data(select_query, params)