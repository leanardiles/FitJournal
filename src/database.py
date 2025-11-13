import mysql.connector #the tool that connects to Aiven MySQL database
from mysql.connector import Error, pooling #the Error class catches and handles database errors (like "connection failed" or "wrong password")
import os #needed to read environment variables (like your database password from .env
from dotenv import load_dotenv # Imports a function that reads .env files so the code can access DB_HOST, DB_PASSWORD, etc. from the .env file

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'ssl_disabled': False  # Aiven requires SSL
}

# Connection pool
connection_pool = pooling.MySQLConnectionPool(
    pool_name="fitjournal_pool",
    pool_size=5,
    pool_reset_session=True,
    **DB_CONFIG
)

def get_db_connection():
    """
    Get a database connection from the pool
    Returns: MySQL connection object
    """
    try:
        connection = connection_pool.get_connection()
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error getting connection from pool: {e}")
        raise

def get_db():
    """
    Dependency for FastAPI routes
    Yields a database connection and ensures it's closed after use
    """
    connection = get_db_connection()
    try:
        yield connection
    except Exception as e:
        print(f"Database error: {e}")
        connection.rollback()
        raise
    finally:
        if connection.is_connected():
            connection.close()

def test_connection():
    """
    Test database connection
    Returns True if successful, False otherwise
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"Successfully connected to MySQL version: {version[0]}")
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return False

# Test connection when module is imported (optional)
if __name__ == "__main__":
    test_connection()