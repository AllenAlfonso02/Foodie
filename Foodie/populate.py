import MySQLdb

host = "localhost"
user = "root"
password = "[EveryGoodHorseEats99Carrots]"

db = MySQLdb.connect(host=host, user=user, passwd=password)
cursor = db.cursor()
msg = 'Test values added successfully.'

cursor.execute('USE Foodie;')

# Adding dummy data
try:
    cursor.execute("""INSERT INTO customer (username, email, password, first_name, last_name, phone_number, city, state, postal_code, country) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", 
                ("bmyers", "b1234@gmail.com", "123", "Bob", "Myers", "8001234567", "Tallahassee", "FL", "32304", "United States"))
    
    cursor.execute("""INSERT INTO customer (username, email, password, first_name, last_name, phone_number, city, state, postal_code, country) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
                ("jdoe", "janedoe@gmail.com", "password", "Jane", "Doe", "8004110000", "Tallahassee", "FL", "32303", "United States"))
    
    cursor.execute("""INSERT INTO customer (username, email, password, first_name, last_name, phone_number, city, state, postal_code, country) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
                ("ehkrabs", "mrkrabs@gmail.com", "secretformula", "Mr", "Krabs", "9991234567", "Bikini Bottom", "FL", "32316", "United States"))

    
    target_username = 'bmyers'
    cursor.execute("SELECT id FROM customer WHERE username=%s", (target_username,))
    target_id = cursor.fetchone()
    
    cursor.execute("""INSERT INTO restaurants (user_id, name, estabImg, address, city, state, postal_code, country, phone_number, website, cuisine_type, price_range, opening_hours, closing_hours) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", 
                (target_id, "Chipotle Mexican Grill", "https://fastly.4sqi.net/img/general/width960/37897634_TE7e10vFyZQCr0DRCXU5YOQ66YAtRnhS3lavKaEBFJs.jpg", "1801 W Tennessee St", "Tallahassee", "FL", "32304", "United States", "8502549986", "https://locations.chipotle.com/fl/tallahassee/1801-w-tennessee-st?utm_source=google&utm_medium=yext&utm_campaign=yext_listings", "Mexican", "$10-$20", "10:45", "22:00"))

    target_username = 'ehkrabs'
    cursor.execute("SELECT id FROM customer WHERE username=%s", (target_username,))
    target_id = cursor.fetchone()    

    cursor.execute("""INSERT INTO restaurants (user_id, name, estabImg, address, city, state, postal_code, country, phone_number, website, cuisine_type, price_range, opening_hours, closing_hours) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", 
                (target_id, "Krusty Krab", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/The_Krusty_Krab.png/1167px-The_Krusty_Krab.png?20231003021001", "831 Bottom Feeder Lane", "Bikini Bottom", "FL", "32315", "United States", "1234567890", "https://spongebob.fandom.com/wiki/Krusty_Krab", "American", "$10-$20", "10:00", "22:00"))

    db.commit()
except Exception as e:
    db.rollback()
    msg = 'Error with inserting dummy values: ' + str(e)

print(msg)
db.close()
