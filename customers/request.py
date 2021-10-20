import sqlite3
import json
from models import Customer, customer


CUSTOMERS = [
     {
            "id": 1,
            "name": "Santa Clasue",
            "address": "2076 N Pole Blvd",
            "email": "hollyjolly@clause.com",
            "password": "gifts"
        },
        {
            "id": 2,
            "name": "Mr. President",
            "address": "1600 Penn Ave",
            "email": "theone@gov.gov",
            "password": "idk"
        }
]

def get_customers():
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            customer.id,
            customer.name,
            customer.address,
            customer.email,
            customer.password
        FROM Customer
        """)
        customers = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'], row['password'])
            customers.append(customer.__dict__)
    return json.dumps(customers)

def get_single_customer(id):
    with sqlite3.connect("./kennel.db")as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            customer.id,
            customer.name,
            customer.address,
            customer.email,
            customer.password
        FROM Customer
        WHERE customer.id = ?
        """, (id, ))
        data = db_cursor.fetchone()
        customer = Customer(data['id'], data['name'], data['address'], data['email'], data['password'])
    return json.dumps(customer.__dict__)

def create_customer(customer):
    max_id = CUSTOMERS[-1]["id"]
    new_id = max_id + 1
    customer["id"] = new_id
    CUSTOMERS.append(customer)
    return customer

def delete_customer(id):
    customer_index = -1
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
           customer_index = index
    if  customer_index >= 0:
        CUSTOMERS.pop(customer_index)

def update_customer(id, new_customer):
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            CUSTOMERS[index] = new_customer
            break

def get_customers_by_email(email):

    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        WHERE c.email = ?
        """, ( email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'] , row['password'])
            customers.append(customer.__dict__)

    return json.dumps(customers)
