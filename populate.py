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
    #LOGIN=======================
    
    cursor.execute("""INSERT INTO login (name, password, type) VALUES (%s,%s,%s);""", ("bmyers","123", "Establishment"))
    cursor.execute("""INSERT INTO login (name, password, type) VALUES (%s,%s,%s);""", ("jdoe","password", "User"))
    cursor.execute("""INSERT INTO login (name, password, type) VALUES (%s,%s,%s);""", ("ehkrabs","secretformula", "Establishment"))

    #CUSTOMERS===================
    cursor.execute('SELECT id FROM login WHERE name=\'bmyers\'')
    login_id = cursor.fetchone()
    
    cursor.execute("""INSERT INTO customer (login_id, first_name, last_name, phone_number, city, state, postal_code, country) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s);""", 
                (login_id,"Bob", "Myers", "(800) 123-4567", "Tallahassee", "FL", "32304", "United States"))
    
    cursor.execute('SELECT id FROM login WHERE name=\'jdoe\'')
    login_id = cursor.fetchone()
    
    cursor.execute("""INSERT INTO customer (login_id, first_name, last_name, phone_number, city, state, postal_code, country) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s);""",
                (login_id,"Jane", "Doe", "(800) 411-0000", "Tallahassee", "FL", "32303", "United States"))
    
    cursor.execute('SELECT id FROM login WHERE name=\'ehkrabs\'')
    login_id = cursor.fetchone()
    cursor.execute("""INSERT INTO customer (login_id, first_name, last_name, phone_number, city, state, postal_code, country) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s);""",
                (login_id,"Mr", "Krabs", "(999) 123-4567", "Bikini Bottom", "FL", "32316", "United States"))

    #RESTAURANTS==================
    
    user = 'bmyers'
    cursor.execute("SELECT id FROM login WHERE name=%s", (user,))
    target_id = cursor.fetchone()
    
    cursor.execute("""INSERT INTO restaurants (user_id, name, estabImg, address, city, state, postal_code, country, phone_number, website, cuisine_type, price_range, opening_hours, closing_hours) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", 
                (target_id, "Chipotle Mexican Grill", "https://fastly.4sqi.net/img/general/width960/37897634_TE7e10vFyZQCr0DRCXU5YOQ66YAtRnhS3lavKaEBFJs.jpg", "1801 W Tennessee St", "Tallahassee", "FL", "32304", "United States", "(850) 254-9986", "https://locations.chipotle.com/fl/tallahassee/1801-w-tennessee-st?utm_source=google&utm_medium=yext&utm_campaign=yext_listings", "Mexican", "$10-$20", "10:45", "22:00"))

    user = 'jdoe'
    cursor.execute("SELECT id FROM login WHERE name=%s", (user, ))
    target_id = cursor.fetchone()

    cursor.execute("""INSERT INTO restaurants (user_id, name, estabImg, address, city, state, postal_code, country, phone_number, website, cuisine_type, price_range, opening_hours, closing_hours) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", 
                (target_id, "The Edison", "https://www.connarchitects.com/wp-content/uploads/2019/09/CONN_Edison-2.jpg", "470 Suwannee St", "Tallahassee", "FL", "32301", "United States", "(850) 765-9771", "https://www.edisontally.com/menu/", "American", "$20-$30", "16:00", "21:00"))


    user = 'ehkrabs'
    cursor.execute("SELECT id FROM login WHERE name=%s", (user,))
    target_id = cursor.fetchone()    
    
    cursor.execute("""INSERT INTO restaurants (user_id, name, estabImg, address, city, state, postal_code, country, phone_number, website, cuisine_type, price_range, opening_hours, closing_hours) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", 
                (target_id, "Krusty Krab", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/The_Krusty_Krab.png/1167px-The_Krusty_Krab.png?20231003021001", "831 Bottom Feeder Lane", "Bikini Bottom", "FL", "32315", "United States", "(123)456-7890", "https://spongebob.fandom.com/wiki/Krusty_Krab", "American", "$10-$20", "10:00", "22:00"))

    #MENU_ITEMS=======================
    first = 'Chipotle Mexican Grill'
    cursor.execute('SELECT id FROM restaurants WHERE name=%s', (first,))
    rest_id = cursor.fetchone()
    
    cursor.execute("INSERT INTO menu_items (restaurant_id, name, foodurl, description, price) VALUES (%s,%s,%s,%s,%s);",
                   (rest_id, "FoodItem", "https", "words words words", 10.99))
    
    cursor.execute("INSERT INTO menu_items (restaurant_id, name, foodurl, description, price) VALUES (%s,%s,%s,%s,%s);",
                   (rest_id, "FoodItem2", "https", "words words words words", 11.99))
    
    cursor.execute("INSERT INTO menu_items (restaurant_id, name, foodurl, description, price) VALUES (%s,%s,%s,%s,%s);",
                   (rest_id, "FoodItem3", "https", "words words words words words", 12.99))    
    
    #LIKED_RESTAURANTS================
    
    first = 'Chipotle Mexican Grill'
    cursor.execute('SELECT id FROM restaurants WHERE name=%s', (first,))
    rest_id = cursor.fetchone()
    cursor.execute('SELECT id FROM customer WHERE first_name=\'Mr\' AND last_name=\'Krabs\'')
    target_id = cursor.fetchone()
    #mr krabs likes chipotle 
    cursor.execute("""INSERT INTO liked_restaurants (user_id, restaurant_id)    
                VALUES (%s,%s);""", 
                (target_id, rest_id))
    
    cursor.execute('SELECT id FROM customer WHERE first_name=\'Jane\' AND last_name=\'Doe\'')
    target_id = cursor.fetchone()
    
    #Jane doe likes chipotle
    cursor.execute("""INSERT INTO liked_restaurants (user_id, restaurant_id) 
                VALUES (%s,%s);""", 
                (target_id, rest_id))

    cursor.execute('SELECT id FROM restaurants WHERE name=\'Krusty Krab\'')
    rest_id = cursor.fetchone()
    
    #Jane doe likes krusty krab
    cursor.execute("""INSERT INTO liked_restaurants (user_id, restaurant_id) 
                VALUES (%s,%s);""", 
                (target_id, rest_id))

    db.commit()

except Exception as e:
    db.rollback()
    msg = 'Error with inserting dummy values: ' + str(e)

print(msg)
db.close()
