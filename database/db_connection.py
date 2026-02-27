import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="hmpandya528@",
            database="goalfit_ai",
            autocommit=True   # IMPORTANT
        )

        print("Database connected successfully!")
        return connection

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None