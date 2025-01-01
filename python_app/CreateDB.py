import mysql.connector
from mysql.connector import Error
import time
import logging
import os

# configure env variables
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost') 
MYSQL_USER = os.getenv('MYSQL_USER', 'root') 
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Sopas_de_aj8!') 

# configure logging
log_file = "app/logs/execution.log"

logging.basicConfig(
    filename=log_file,  # file path
    level=logging.INFO,  # INFO logging level - used for INFO and ERROR
    format='%(asctime)s - %(levelname)s - %(message)s'  # log message format
)

max_retries = 5
retry_count = 0
connection = None

while retry_count < max_retries:
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )

        # If connected, log the success and break the loop
        if connection.is_connected():
            logging.info("Connected to MySQL server")

            cursor = connection.cursor()

            # Create the database if it doesn't exist
            database_name = "Mira_Transfermarkt"
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            logging.info(f"Database '{database_name}' created or already exists.")

            # Exit the loop if connection is successful
            break

    except Error as e:
        logging.error(f"Error creating the Database: {e}")

        # If we haven't tried 5 times, wait and retry
        retry_count += 1
        if retry_count < max_retries:
            logging.info(f"Retrying in 10 seconds... (Attempt {retry_count + 1}/{max_retries})")
            time.sleep(10)
        else:
            logging.error("Max retries reached. Could not connect to MySQL.")
            break

# Close the connection if it was successful
if connection and connection.is_connected():
    connection.close()
    logging.info("MySQL connection closed.")


