import MySQLdb

host = "localhost"
user = "root"
password = ""

db = MySQLdb.connect(host=host, user=user, passwd=password)
cursor = db.cursor()
msg = 'Test values added successfully.'

cursor.execute('USE Foodie;')

# Adding dummy data
try:
    cursor.execute("""INSERT INTO customer (username, email, password, first_name, last_name, phone_number, city, state, postal_code, country) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s);""", 
                ("BMyers", "b1234@gmail.com", "123", "Bob", "Myers", "8001234567", "Tallahassee", "FL", "32304", "United States"))

    cursor.execute("""INSERT INTO restaurants (user_id, name, estabImg, address, city, state, postal_code, country, phone_number, website, cuisine_type, price_range, opening_hours, closing_hours) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", 
                (1, "Chipotle Mexican Grill", "https://fastly.4sqi.net/img/general/width960/37897634_TE7e10vFyZQCr0DRCXU5YOQ66YAtRnhS3lavKaEBFJs.jpg", "1801 W Tennessee St", "Tallahassee", "FL", "32304", "United States", "8502549986", "https://locations.chipotle.com/fl/tallahassee/1801-w-tennessee-st?utm_source=google&utm_medium=yext&utm_campaign=yext_listings", "Mexican", "$10-$20", "10:45", "22:00"))

    cursor.execute("""INSERT INTO restaurants (user_id, name, estabImg, address, city, state, postal_code, country, phone_number, website, cuisine_type, price_range, opening_hours, closing_hours) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", 
                (1, "Krusty Krab", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/The_Krusty_Krab.png/1167px-The_Krusty_Krab.png?20231003021001", "831 Bottom Feeder Lane", "Tallahassee", "FL", "32304", "United States", "1234567890", "https://spongebob.fandom.com/wiki/Krusty_Krab", "American", "$10-$20", "10:00", "22:00"))

    db.commit()
except:
    db.rollback()
    msg = 'Error with inserting dummy values.'

print(msg)
db.close()