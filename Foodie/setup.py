import MySQLdb

# Database connection parameters
host = "localhost"
user = "root"
password = "Abeticabted14837!("

db = MySQLdb.connect(host=host, user=user, passwd=password)
cursor = db.cursor()

# Create a new database
cursor.execute("CREATE DATABASE IF NOT EXISTS Foodie;")
print("Database 'Foodie' created successfully.")

# Select the newly created database
cursor.execute("USE Foodie;")

# Create a new table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS login (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        password VARCHAR(100),
        type VARCHAR(100)
    ); 
    """)
print("Table 'login' created successfully.")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        estabImg VARCHAR(255), 
        address VARCHAR(255) NOT NULL,
        city VARCHAR(100) NOT NULL,
        state VARCHAR(100) NOT NULL,
        postal_code VARCHAR(20),
        country VARCHAR(100) NOT NULL,
        phone_number VARCHAR(20),
        website VARCHAR(255),
        cuisine_type VARCHAR(100),
        price_range VARCHAR(50),
        opening_hours VARCHAR(255),
        closing_hours VARCHAR(255)
);
""")
print("Table 'restaurants' created successfully.")

cursor.execute("""
CREATE TABLE IF NOT EXISTS customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20),
    country VARCHAR(100) NOT NULL
);
""")
print("Table 'customer' created successfully.")

cursor.execute("""
CREATE TABLE if NOT EXISTS  menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    foodurl VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);
""")
print("Table 'menu_items' created successfully.")

cursor.execute("""
CREATE TABLE IF NOT EXISTS liked_restaurants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES customer(id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);
""")
print("Table 'liked_restaurants' created successfully.") 

cursor.execute("CREATE ROLE IF NOT EXISTS 'Establishment'")
cursor.execute("CREATE ROLE IF NOT EXISTS 'Restaurant_user'")

cursor.execute("CREATE ROLE IF NOT EXISTS 'customer_user'")
cursor.execute("CREATE ROLE IF NOT EXISTS 'restaurant_user'")
cursor.execute("CREATE ROLE IF NOT EXISTS 'admin'")

roles_command = [
    "GRANT SELECT ON Foodie.restaurants TO 'customer_user';",
    "GRANT SELECT ON Foodie.menu_items TO 'customer_user';",
    "GRANT SELECT, INSERT, UPDATE ON Foodie.customer TO 'customer_user';",
    "GRANT SELECT, INSERT, UPDATE, DELETE ON Foodie.restaurants TO 'restaurant_user';",
    "GRANT SELECT, INSERT, UPDATE, DELETE ON Foodie.menu_items TO 'restaurant_user';",
]

#for command in roles_command:
#    cursor.execute(command)

cursor.execute("SET ROLE ALL;")
#cursor.execute("SET ROLE 'customer_user';")
#cursor.execute("SET ROLE 'restaurant_user';")

print("Roles set up")
