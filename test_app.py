# import all necessary modules 
import os
import unittest
import MySQLdb
from dotenv import load_dotenv
import app
#import pytest 

# Load environment variables from .env file
load_dotenv()
#@pytest_fixture
class TestEvents(unittest.TestCase): 
    def setUp(self):
        # Set up a connection to the database
        self.connection = MySQLdb.connect(
            host=os.getenv("hostname"),
            user=os.getenv("username"),
            passwd=os.getenv("password"),
            db=os.getenv("database"),
            ssl={
                "ssl_ca": "/etc/ssl/cert.pem"
            }
        )
        
        # test data 

        #app.create_event("roll","2023-06-15 18:30:00","2023-09-01 20:00:00","home")



        # Create a cursor object for executing SQL queries
        self.cursor = self.connection.cursor()

    def tearDown(self):
        # Close the database connection after each test
        self.connection.close()
        # request.addfinalizer()

    def test_create_event(self):
        # Happy path test for create_event function 
        is_created = False
        app.create_event("push ","2023-06-15 18:30:00","2023-09-01 20:00:00","home")
        is_created = True
        print("the event has been created ")
        if is_created == False:
            self.assertRaises(ValueError)

    def test_delete_event(self):
        # TODO: write test for delete_event function
        pass

    def test_list_events(self):
        # TODO: write test for list_events function
        pass

    def test_edit_event(self):
        # TODO: write test for edit_event function
        pass

if __name__ == "__main__":
    unittest.main()