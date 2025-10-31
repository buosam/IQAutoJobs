
import sys
import os
from sqlalchemy import create_engine, text
from app.db.models import Base
# This ensures the script can find the 'app' module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
# Load the .env file from the backend directory
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)


# Now that .env is loaded, we can import the database modules
# which rely on the settings being correctly populated
from app.core.config import Settings
from sqlalchemy.engine.url import make_url

def reset_database():
    """Drops and recreates all tables."""
    print("Connecting to the database...")
    settings = Settings(_env_file=dotenv_path)

    sync_url = make_url(settings.DATABASE_URL)
    if sync_url.drivername.endswith('+asyncpg'):
        sync_url = sync_url.set(drivername=sync_url.drivername.removesuffix('+asyncpg'))
    engine = create_engine(sync_url)

    with engine.connect() as connection:
        with connection.begin():
            print("Dropping public schema with cascade...")
            connection.execute(text('DROP SCHEMA public CASCADE;'))
            print("Creating public schema...")
            connection.execute(text('CREATE SCHEMA public;'))

    print("Creating all tables from metadata...")
    Base.metadata.create_all(engine)
    print("Tables created.")

    print("Database has been reset.")

if __name__ == "__main__":
    reset_database()
