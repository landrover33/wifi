import subprocess
from typing import Dict, Union
from persistent import Persistent
import time

from BTrees.OOBTree import OOBTree
import os
from ZODB import FileStorage, DB
import transaction
from persistent import Persistent


# ====================  classes  ==================================

class Wifi(Persistent):
    def __init__(self, id, Name, Description, GUID, Physical_address, State, SSID, BSSID, Network_type,
                 Radio_type, Authentication, Cipher, Connection_mode, Channel, Receive_rate, Transmit_rate,
                 Signal, Profile, Hosted_network_status, timestamp):
        self.id = id
        self.Name = Name
        self.Description = Description
        self.GUID = GUID
        self.Physical_address = Physical_address
        self.State = State
        self.SSID = SSID
        self.BSSID = BSSID
        self.Network_type = Network_type
        self.Radio_type = Radio_type
        self.Authentication = Authentication
        self.Cipher = Cipher
        self.Connection_mode = Connection_mode
        self.Channel = Channel
        self.Receive_rate = Receive_rate
        self.Transmit_rate = Transmit_rate
        self.Signal = Signal
        self.Profile = Profile
        self.Hosted_network_status = Hosted_network_status
        self.timestamp = timestamp

    def __str__(self):
        attributes = [
            f"ID: {self.id}",
            f"Name: {self.Name}",
            f"Description: {self.Description}",
            f"GUID: {self.GUID}",
            f"Physical Address: {self.Physical_address}",
            f"State: {self.State}",
            f"SSID: {self.SSID}",
            f"BSSID: {self.BSSID}",
            f"Network Type: {self.Network_type}",
            f"Radio Type: {self.Radio_type}",
            f"Authentication: {self.Authentication}",
            f"Cipher: {self.Cipher}",
            f"Connection Mode: {self.Connection_mode}",
            f"Channel: {self.Channel}",
            f"Receive Rate (Mbps): {self.Receive_rate}",
            f"Transmit Rate (Mbps): {self.Transmit_rate}",
            f"Signal: {self.Signal}",
            f"Profile: {self.Profile}",
            f"Hosted Network Status: {self.Hosted_network_status}",
            f"Time Stamp: {self.timestamp}"
        ]
        return "\n".join(attributes)


# ====================  zodb crud  ==================================

def create_wifi_table():
    table_name = 'wifi_reading'
    # Get the current file directory
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = 'wifi_db.fs'
    # Set the database file path and name
    database_path = os.path.join(current_file_dir, db_name)

    # Create the ZODB file storage and database
    storage = FileStorage.FileStorage(database_path)
    db = DB(storage)
    connection = db.open()

    # Get the root object of the database
    root = connection.root()

    # Check if the wifi_reading table exists
    if table_name not in root:
        # Create the wifi_reading table if it doesn't exist
        root[table_name] = {}

        # Commit the transaction
        transaction.commit()
        print(f"Table named \"{table_name}\" created.")
    else:
        print("Table exists.")
    # Close the connection
    connection.close()
    db.close()


def insert_wifi_instance_in_DB(wifi_instance):
    # Open the ZODB database
    storage = FileStorage.FileStorage('wifi_db.fs')
    db = DB(storage)
    connection = db.open()

    # Get the root object of the database
    root = connection.root()

    # Check if the 'wifi_reading' table exists
    if 'wifi_reading' not in root:
        # Create a new OOBTree to store the Wifi instances
        root['wifi_reading'] = OOBTree()

    # Get the OOBTree for 'wifi_reading'
    wifi_reading_table = root['wifi_reading']

    # Generate a unique ID for the Wifi instance
    wifi_instance_id = len(wifi_reading_table) + 1

    # Set the ID of the Wifi instance
    wifi_instance.id = wifi_instance_id

    # Add the Wifi instance to the 'wifi_reading' table
    wifi_reading_table[wifi_instance_id] = wifi_instance

    # Commit the transaction
    transaction.commit()

    # Close the connection and database
    connection.close()
    db.close()


# ====================  business functions  ==================================

def get_wifi_details() -> Union[Dict[str, str], Dict[str, Union[str, int]]]:
    command: str = 'netsh wlan show interfaces'
    result = subprocess.run(
        command, capture_output=True, text=True, shell=True)

    output: str = result.stdout.strip()
    error: str = result.stderr.strip()

    wifi_details: Dict[str, Union[str, int]] = {}

    if output:
        lines = output.splitlines()
        for line in lines:
            if line.strip():
                key, value = line.split(":", 1)
                wifi_details[key.strip()] = value.strip()
    else:
        wifi_details["error"] = error

    return wifi_details


def create_wifi_instance(properties):
    id = 1  # Set the id value (you can adjust this as needed)

    # Extract the properties from the dictionary
    Name = properties.get('Name', '')
    Description = properties.get('Description', '')
    GUID = properties.get('GUID', '')
    Physical_address = properties.get('Physical address', '')
    State = properties.get('State', '')
    SSID = properties.get('SSID', '')
    BSSID = properties.get('BSSID', '')
    Network_type = properties.get('Network type', '')
    Radio_type = properties.get('Radio type', '')
    Authentication = properties.get('Authentication', '')
    Cipher = properties.get('Cipher', '')
    Connection_mode = properties.get('Connection mode', '')
    Channel = int(properties.get('Channel', 0))
    Receive_rate = float(properties.get('Receive rate (Mbps)', 0))
    Transmit_rate = float(properties.get('Transmit rate (Mbps)', 0))
    # Remove '%' character
    Signal = int(properties.get('Signal', 0).rstrip('%'))
    Profile = properties.get('Profile', '')
    Hosted_network_status = properties.get('Hosted network status', '')
    timestamp = int(time.time())

    # Create an instance of the Wifi class with the extracted properties
    wifi_instance = Wifi(id, Name, Description, GUID, Physical_address, State, SSID, BSSID, Network_type,
                         Radio_type, Authentication, Cipher, Connection_mode, Channel, Receive_rate, Transmit_rate,
                         Signal, Profile, Hosted_network_status, timestamp)

    return wifi_instance


# =====================  Main ============================================
db_name = "wifi_db.fs"
create_wifi_table()
# get wifi info
wifi_info = get_wifi_details()

# write to zodb
if "error" in wifi_info:
    print("Error:", wifi_info["error"])
else:
    # print("Wi-Fi Details:")
    wifi_instance = create_wifi_instance(wifi_info)
    print(wifi_instance)
    insert_wifi_instance_in_DB(wifi_instance)
# read from zodb

wifi_instace_list = get_all_wifi_instances(db_name)
