from sqlalchemy import *
import os
from sqlalchemy.engine.reflection import inspect

def create_wifi_table():
    # Get the current file directory
    current_file_dir = os.path.dirname(os.path.abspath(__file__))

    # Set the database file path and name
    database_path = os.path.join(current_file_dir, 'wifi_db.db')

    # Create the engine and connect to the database
    engine = create_engine(f'sqlite:///{database_path}')

    # Define the table metadata
    metadata = MetaData()
    wifi_table = Table('wifi', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('Name', String),
                       Column('Description', String),
                       Column('GUID', String),
                       Column('Physical address', String),
                       Column('State', String),
                       Column('SSID', String),
                       Column('BSSID', String),
                       Column('Network type', String),
                       Column('Radio type', String),
                       Column('Authentication', String),
                       Column('Cipher', String),
                       Column('Connection mode', String),
                       Column('Channel', Integer),
                       Column('Receive rate (Mbps)', Float),
                       Column('Transmit rate (Mbps)', Float),
                       Column('Signal', Integer),
                       Column('Profile', String),
                       Column('Hosted network status', String))

    # Check if the table exists
    inspector = inspect(engine)
    if not inspector.has_table('wifi'):
        # Create the table if it doesn't exist
        metadata.create_all(engine)

# Call the function to create the wifi table if it doesn't exist
create_wifi_table()
