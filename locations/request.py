import json
import sqlite3
from models import Location

LOCATIONS = [
     {
            "id": 1,
            "name": "Nashville North",
            "address": "101 North Nashville Dr"
        },
        {
            "id": 2,
            "name": "Nashville South",
            "address": "912 South Nashville Dr"
        }
]

def get_locations():
    with sqlite3.connect("./kennel.db") as connection:
        connection.row_factory = sqlite3.Row
        db_cursor = connection.cursor()
        db_cursor.execute("""
        SELECT
            location.id,
            location.name,
            location.address
        FROM Location
        """)
        locations = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            location = Location(row['id'], row['name'], row['address'])
            locations.append(location.__dict__)
        return json.dumps(locations)


def get_single_location(id):
    with sqlite3.connect("./kennel.db") as connection:
        connection.row_factory = sqlite3.Row
        db_cursor = connection.cursor()
        db_cursor.execute("""
        SELECT 
            location.id,
            location.name,
            location.address
        FROM Location
        WHERE location.id = ?
        """,(id, ))
        data = db_cursor.fetchone()
        location = Location(data['id'], data['name'], data['address'])
    return json.dumps(location.__dict__)
        
        
def create_location(location):
    max_id = LOCATIONS[-1]["id"]
    new_id = max_id + 1
    location["id"] = new_id
    LOCATIONS.append(location)
    return location

def delete_location(id):
    location_index = -1
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            location_index = index
    if location_index >= 0:
        LOCATIONS.pop(location_index)  

def update_location(id, new_location):
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            LOCATIONS[index] = new_location
            break 