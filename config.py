import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database 
database_name = "UDACasting"
database_url = 'localhost:5432' 
SQLALCHEMY_DATABASE_URI = f'postgresql://:@{database_url}/{database_name}'
