import uuid
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb
import certifi
import os 
import mysql.connector



connection = MySQLdb.connect(
    host= os.getenv("hostname"),
    user= os.getenv("username"),
    passwd= os.getenv("password"),
    db= os.getenv("database"),
    ssl  = {
        "ssl_ca": "/etc/ssl/cert.pem"
    }
)


import mysql.connector

# Create a connection to the MySQL database
connection = mysql.connector.connect(
    host= os.getenv("hostname"),
    user= os.getenv("username"),
    password= os.getenv("password"),
    database= os.getenv("database")
   
)
cursor = connection.cursor()

def create_event(name,start_date,end_date,venue):
    # Task name should not be empty
    if name is None:
        raise ValueError("Name cannot be None")

    # Task name should be unique
    cursor.execute("SELECT * FROM events WHERE event_name = %s", (name,))
    result = cursor.fetchone()
    if result is not None:
        raise ValueError("event name should be unique")

    # Task properties
    event_id = str(uuid.uuid4())
     # Convert start_date and end_date to datetime objects
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD HH:MM:SS")
    venue = venue

    # Insert task into database
    sql = "INSERT INTO events (event_id, event_name, start_date, end_date, venue) VALUES (%s, %s, %s, %s, %s)"
    val = (event_id, name, start_date, end_date, venue)
    cursor.execute(sql, val)
    connection.commit()

    # Retrieve inserted task from database
    cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
    result = cursor.fetchone()

    event = {
        "event_id": result[0],
        "event_name": result[1],
        "start_date": result[2],
        "end_date": result[3],
        "venue": result[4]
    }

    return event


    # function to delete an event with the specific event_id from the database 
def delete_event(event_id):
        # Delete task from database
        cursor.execute("DELETE FROM events WHERE event_id = %s", (event_id,))
        connection.commit()

        return True

# lists all events created in the database 

def list_events():
    cursor.execute("SELECT * FROM events")
    results = cursor.fetchall()
    events = []
    for result in results:
        event = {
            "event_id": result[0],
            "event_name": result[1],
            "start_date": result[2],
            "end_date": result[3],
            "venue": result[4]
        }
        events.append(event)
    print (events)

# a function to edit the event details 
def edit_event(event_id, name=None, start_date=None, end_date=None, venue=None):
    # Ensure that the event_id is not None
    if event_id is None:
        raise ValueError("event_id cannot be None")

    # Check if the event exists in the database
    cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
    result = cursor.fetchone()
    if result is None:
        raise ValueError("Event with event_id %s does not exist" % event_id)

    # Update the event details
    if name is not None:
        cursor.execute("UPDATE events SET event_name = %s WHERE event_id = %s", (name, event_id))
    if start_date is not None:
        cursor.execute("UPDATE events SET start_date = %s WHERE event_id = %s", (start_date, event_id))
    if end_date is not None:
        cursor.execute("UPDATE events SET end_date = %s WHERE event_id = %s", (end_date, event_id))
    if venue is not None:
        cursor.execute("UPDATE events SET venue = %s WHERE event_id = %s", (venue, event_id))

    # Commit the changes to the database
    connection.commit()

    # Retrieve the updated event from the database
    cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
    result = cursor.fetchone()

    updated_event = {
        "event_id": result[0],
        "event_name": result[1],
        "start_date": result[2],
        "end_date": result[3],
        "venue": result[4]
    }

    return updated_event

     
