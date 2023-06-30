import subprocess
from typing import Dict, Union
from persistent import Persistent
import time
import os
from BTrees.OOBTree import OOBTree
from ZODB import FileStorage, DB
import transaction
from typing import List
import uuid
import pprint

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


# ====================  zodb CRUD  ==================================

def create_wifi_instance(connection, wifi_instance: Wifi):
    root = connection.root()

    # Retrieve the wifi_table from the root object
    wifi_table = root.setdefault('wifi_table', OOBTree())

    # Add the wifi_instance to the wifi_table
    wifi_table[wifi_instance.id] = wifi_instance

    # Commit the transaction
    transaction.commit()


def read_wifi_instance(connection, wifi_id):
    root = connection.root()
    wifi_table = root.get('wifi_table', None)

    if wifi_table is not None:
        return wifi_table.get(wifi_id, None)

    return None


def read_all_wifi_instances(connection) -> List[Wifi]:
    root = connection.root()

    # Retrieve all wifi instances from the database
    wifi_table = root.get('wifi_table', None)
    wifi_instances = []

    if wifi_table is not None:
        wifi_instances = list(wifi_table.values())

    return wifi_instances


def update_wifi_instance(connection, wifi_instance: Wifi):
    root = connection.root()
    wifi_table = root.get('wifi_table', None)

    if wifi_table is not None and wifi_instance.id in wifi_table:
        wifi_table[wifi_instance.id] = wifi_instance
        transaction.commit()
        return True

    return False


def delete_wifi_instance(connection, wifi_id):
    root = connection.root()
    wifi_table = root.get('wifi_table', None)

    if wifi_table is not None and wifi_id in wifi_table:
        del wifi_table[wifi_id]
        transaction.commit()
        return True

    return False


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


def convert_dic_to_wifi_instance(properties):
    id = str(uuid.uuid4())

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

# Create the database connection
db_name = "wifi_db.fs"
storage = FileStorage.FileStorage(db_name)
db = DB(storage)
connection = db.open()

# get wifi info
wifi_properties = get_wifi_details()

# write to zodb
if "error" in wifi_properties:
    print("Error:", wifi_properties["error"])
else:
    # print("Wi-Fi Details:")
    wifi_instance = convert_dic_to_wifi_instance(wifi_properties)
    # print(wifi_instance)
    create_wifi_instance(connection, wifi_instance)


# read from zodb

wifi_instances = read_all_wifi_instances(connection)

# Iterate over the wifi instances and print each instance
for wifi_instance in wifi_instances:
    print(wifi_instance)
    # pprint.pprint(wifi_instance.__dict__)
    print()

print(
    f"-----------------------------\nTotal no of Wifi readings: {len(wifi_instances)}")
# Close the connection and clean up resources
connection.close()
db.close()
