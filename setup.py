import MySQLdb

# Database connection parameters
host = "localhost"
user = "root"
password = "septons"

db = MySQLdb.connect(host=host, user=user, passwd=password)
cursor = db.cursor()

# Create a new database
cursor.execute("CREATE DATABASE IF NOT EXISTS login;")
print("Database 'login' created successfully.")

# Select the newly created database
cursor.execute("USE login;")

# Create a new table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS login (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        password VARCHAR(100),
        type VARCHAR(100)
    );
""")
print("Table 'mytable' created successfully.")