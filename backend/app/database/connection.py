import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",       # your MySQL host (local machine)
        port=3306,              # default MySQL port
        user="root",            # your MySQL username
        password="yourpassword",# your MySQL password
        database="my_database"  # your database name
    )
    return connection
