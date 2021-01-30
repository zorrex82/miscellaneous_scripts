# Import libraries to connect in MySQL database
import mysql.connector

# This is a sample function to test connection and validate the info about the database
try:
    connection = mysql.connector.connect(host='localhost',
                                         database='databasename',
                                         user='user_database',
                                         password='password')  # Basic infos to use in database connection
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select * from table_name;")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
    else:
        print('Error in connection database')

finally:
    connection.close()  # Close connection is good practice.
