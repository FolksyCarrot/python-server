import sqlite3
import json
from models import Employee
from models import Location



EMPLOYEES = [
    {
            "id": 1,
            "name": "Luke Skywalker",
            "address": "333 Degoba System",
            "location_id": 1
        },
        {
            "id": 2,
            "name": "Bart Simpson",
            "address": "90 Cartoon Way",
            "location_id": 1
        }
]

def get_employees():
    with sqlite3.connect("./kennel.db") as connection:
        connection.row_factory = sqlite3.Row
        db_cursor = connection.cursor()
        db_cursor.execute("""
        SELECT
            employee.id,
            employee.name,
            employee.address,
            employee.location_id,
            location.name location_name,
            location.address Location_address
        FROM Employee
        JOIN Location
            ON Location.id = Employee.location_id
        """) 
        employees = []
        dataset = db_cursor.fetchall()
        for row in  dataset:
            employee = Employee(row['id'], row['name'], row['address'], row['location_id'])
            location = Location(row['id'], row['location_name'], row['location_address'])

            employee.location = location.__dict__
            employees.append(employee.__dict__)
        return json.dumps(employees)

def get_single_employee(id):
    with sqlite3.connect("./kennel.db") as connection:
        connection.row_factory = sqlite3.Row
        db_cursor = connection.cursor()
        db_cursor.execute("""
        SELECT
            employee.id,
            employee.name,
            employee.address,
            employee.location_id
        FROM Employee
        WHERE employee.id = ?
        """, (id, ))
        data = db_cursor.fetchone()
        employee = Employee(data['id'], data['name'], data['address'], data['location_id'])
    return json.dumps(employee.__dict__)

def create_employee(employee):
    max_id = EMPLOYEES[-1]["id"]
    new_id = max_id + 1
    employee["id"] = new_id
    EMPLOYEES.append(employee)
    return employee

def delete_employee(id):
    employee_index = -1
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
           employee_index = index
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)

def update_employee(id, new_employee):
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            EMPLOYEES[index] = new_employee
            break

def find_employees_by_location(location):
    with sqlite3.connect("./kennel.db") as connection:
        connection.row_factory = sqlite3.Row
        db_cursor = connection.cursor()
        db_cursor.execute("""
        SELECT
            employee.id,
            employee.name,
            employee.address,
            employee.location_id
        FROM Employee
        WHERE employee.location_id = ?
        """, (location, ))
        employees = []
        data = db_cursor.fetchall()

    for row in data:
        employee = Employee(row['id'], row['name'], row['address'], row['location_id'])
        employees.append(employee.__dict__)
    return json.dumps(employees)