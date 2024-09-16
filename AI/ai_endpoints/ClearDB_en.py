from sqlalchemy import create_engine, MetaData

# Database URL
database_url = 'sqlite:///aibookeditordata_en.db'

# Create a new SQLAlchemy engine
engine = create_engine(database_url)

# Create a MetaData instance to load the schema
metadata = MetaData()

# Reflect the existing tables into metadata
metadata.reflect(bind=engine)

# Connect to the database
with engine.connect() as connection:
    # Drop all tables (which will clear all the data)
    metadata.drop_all(connection)
    print("All tables have been dropped (data cleared).")

    # Recreate the tables (this step assumes you want to preserve the schema)
    metadata.create_all(connection)
    print("All tables have been recreated.")
