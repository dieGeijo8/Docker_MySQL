import mysql.connector
from mysql.connector import Error
import os
import logging

# configure env variables
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost') 
MYSQL_USER = os.getenv('MYSQL_USER', 'root') 
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Sopas_de_aj8!') 
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'Mira_Transfermarkt') 
MYSQL_PORT = 3306

# configure logging
log_file = "/app/logs/execution.log"

logging.basicConfig(
    filename=log_file,  # file path
    level=logging.INFO,  # INFO logging level - used for INFO and ERROR
    format='%(asctime)s - %(levelname)s - %(message)s'  # log message format
)

try:
    # Connect to the database
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        port=MYSQL_PORT
    )

    if connection.is_connected():
        cursor = connection.cursor()
except Exception as e:
    logging.error(f"Error in the connection with the DB: {e}")

try:
    # Start a transaction - either all tables are created or no table is created
    connection.start_transaction()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS teams_table (
        Team_ID INT NOT NULL,
        Team_name VARCHAR(255) NOT NULL,
        PRIMARY KEY (Team_ID)
    );
    """

    cursor.execute(create_table_query)
    logging.info("Table 'teams_table' created successfully.")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS transfers_table (
        Player_ID INT NOT NULL,
        Player_Name VARCHAR(255) NOT NULL,
        Acquiring_team_ID INT NOT NULL,
        Acquiring_team_name VARCHAR(255) NOT NULL,
        Selling_team_ID INT NOT NULL,
        Selling_team_name VARCHAR(255) NOT NULL,
        Price BIGINT NOT NULL,
        Description TEXT,
        PRIMARY KEY (Player_ID, Acquiring_team_ID, Selling_team_ID)
    );
    """

    cursor.execute(create_table_query)
    logging.info("Table 'transfers_table' created successfully.")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS players_table (
        Team_ID INT NOT NULL,
        Player_ID INT NOT NULL,
        Player_name VARCHAR(255) NOT NULL,
        PRIMARY KEY (Player_ID, Team_ID)
    );
    """
    cursor.execute(create_table_query)
    logging.info("Table 'players_table' created successfully.")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS market_values_table (
        Team_ID INT NOT NULL,
        Team_name VARCHAR(255) NOT NULL,
        Player_ID INT NOT NULL,
        Player_name VARCHAR(255) NOT NULL,
        Market_value INT,
        PRIMARY KEY (Player_ID, Team_ID)
    );
    """
    cursor.execute(create_table_query)
    logging.info("Table 'market_values_table' created successfully.")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS injuries_table (
        Player_ID INT NOT NULL,
        Player_name VARCHAR(255),
        Injury VARCHAR(255),
        Start_date DATE,
        End_date DATE,
        Games_missed INT,
        Team_ID INT NOT NULL,
        PRIMARY KEY (Player_ID, Start_date, End_date)
    );
    """
    cursor.execute(create_table_query)
    logging.info("Table 'injuries table' created successfully.")

    # Commit the transaction
    connection.commit()
    logging.info("All tables created successfully, transaction committed.")
except Error as e:
    connection.rollback()
    logging.error(f"Error creating tables in the DB, transaction rolled back: {e}")

if connection and connection.is_connected():
    connection.close()
    logging.info("MySQL connection closed.")

