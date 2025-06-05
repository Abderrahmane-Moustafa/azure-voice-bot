import pyodbc
from config import settings

def get_db_connection():
    conn_str = f"""
    DRIVER={{ODBC Driver 17 for SQL Server}};
    SERVER={settings.sql_server};
    DATABASE={settings.sql_database};
    UID={settings.sql_username};
    PWD={settings.sql_password};
    Encrypt=yes;
    TrustServerCertificate=no;
    Connection Timeout=30;
    """
    return pyodbc.connect(conn_str)

def save_user_to_db(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO users (first_name, last_name, birth_date, email, phone, street, city, country, postal_code)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (
        data.get("firstName"),
        data.get("lastName"),
        data.get("birthDate"),
        data.get("email"),
        data.get("phoneNumber"),
        data.get("street"),
        data.get("city"),
        data.get("country"),
        data.get("postalCode")
    ))
    conn.commit()
    conn.close()


'''import sqlite3

DB_NAME = "userdb.sqlite"

# Ensure the DB file exists and has the table
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            birth_date TEXT,
            email TEXT,
            phone TEXT,
            street TEXT,
            postal_code TEXT,
            city TEXT,
            country TEXT
        )
    """)
    conn.commit()
    conn.close()

# Call it once when starting the app
init_db()

def save_user_to_db(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = """
        INSERT INTO users (first_name, last_name, birth_date, email, phone, street, postal_code, city, country)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (
        data.get("firstName"),
        data.get("lastName"),
        data.get("birthDate"),
        data.get("email"),
        data.get("phoneNumber"),
        data.get("street"),
        data.get("postalCode"),
        data.get("city"),
        data.get("country")
    ))
    conn.commit()
    conn.close()
'''