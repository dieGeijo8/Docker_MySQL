# Prerequisites

To run this project, make sure Docker is installed on your machine and that no processes are occupying port 3306, which is the default port used by MySQL.

This project creates two Docker containers:
1. **Python Container**: Executes scripts to create a MySQL database with five tables and populates them with data scraped from Transfermarkt.
2. **MySQL Container**: Hosts the created MySQL database.

The database is configured to be accessible from your local machine as well. However, to enable this functionality MySQL must be installed locally.  

If MySQL is not installed on your local machine, you can still access the database from within either of the two containers created, as detailed below.

The variables used to connect to MySQL are defined in the Docker files and can be modified there. Detailed information about the execution of the Python scripts is logged in the `logs/execution.log` file inside the Python container.

# How to Run

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/dieGeijo8/Docker_MySQL.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Docker_MySQL
   ```
3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
Once the containers are running, you can query the database from various environments. 

### Query the Database from Inside the MySQL Container:
1. List the running containers:
   ```bash
   docker ps
   ```
2. Open a shell in the MySQL container:
   ```bash
   docker exec -it <container_name_or_id> /bin/bash
   ```
3. Access the MySQL database:
   ```bash
   mysql -u root -p
   ```

### Query the Database from Inside the Python Container
1. Open a shell in the Python container:
  ```bash
   mysql -u root -p -h localhost -P 3306
   ```
2. Run the example query script:
  ```bash
   python ExampleQueries_fromLocalURI.py
   ```
This script connects to the database using a local URI and prints the first 10 rows from each table.

### Query the database from your local machine
1. Ensure MySQL is installed and not using port 3306 for other processes.
2. Access the database:
   ```bash
   mysql -u root -p -h localhost -P 3306
   ```