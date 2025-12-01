from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Create database URL for SQLAlchemy
# Format: mysql+pymysql://user:password@host:port/database
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
# echo=True shows SQL queries in console (useful for debugging, set to False in production)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600,   # Recycle connections after 1 hour
    echo=True            # Set to False in production
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    """
    Dependency that provides a database session to FastAPI routes.
    Automatically closes the session after the request is complete.
    
    Usage in routes:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            users = db.query(User).all()
            return users
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test connection function (optional, for debugging)
def test_connection():
    """
    Test database connection
    Returns True if successful, False otherwise
    """
    try:
        # Try to connect
        connection = engine.connect()
        print("✓ Successfully connected to MySQL database")
        
        # Test a simple query
        result = connection.execute("SELECT VERSION()")
        version = result.fetchone()
        print(f"✓ MySQL version: {version[0]}")
        
        connection.close()
        return True
    except Exception as e:
        print(f"✗ Error connecting to MySQL: {e}")
        return False

# Test connection when running this file directly
if __name__ == "__main__":
    test_connection()