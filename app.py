import MySQLdb
from flask import Flask, render_template, request, jsonify, redirect, url_for
import MySQLdb.cursors
import bcrypt



app = Flask(__name__)

currentID = 0
rootpswd = 'septons'   #ENTER ROOT PASS HERE

# Database connection parameters
class mySQLClass:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.database = "Foodie"
        self.cursor = None
        self.connection = None

    def connect(self):
        self.connection = MySQLdb.connect(
            host=self.host, user=self.user, password=self.password, database=self.database
        )
        self.cursor = self.connection.cursor()
        return self.connection

    def change(self, user, password):
        self.user = user
        self.password = password

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


db = mySQLClass("localhost", "root", rootpswd)
db.connect()


@app.route('/')
def home():
    return render_template('startingPage.html')

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    print("in here?")
    db.close()
    db.change("root", rootpswd)
    db.connect()
    if (request.method == 'POST'):

        user = request.form['userNameOrEmail']
        passWrd = request.form['userPassword']

        print(user)
        print(passWrd)

        try:



            db.cursor.execute("SELECT password FROM login WHERE name = %s", (user,))

            result = db.cursor.fetchone()

            if result:
                stored_hashed_password = result[0]
                if bcrypt.checkpw(passWrd.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    "Shows the grants for each user"
                    show_grants_query = "SHOW GRANTS FOR %s@'localhost'"
                    db.cursor.execute(show_grants_query, (user,))
                    privileges = db.cursor.fetchall()

                    for privilege in privileges:
                        print(privilege)
                        "manually input the privileges  "

                    #TESTING HERE
                    db.cursor.execute("SELECT type FROM login WHERE name = %s", (user,))
                    result = db.cursor.fetchone()

                    if result[0] == "User":
                        db.cursor.execute("GRANT 'customer_user' TO %s@'localhost';", (user,))
                        print("Grants granted for user")
                    elif result[0] == "Establishment":
                        db.cursor.execute("GRANT 'restaurant_user' TO %s@'localhost';", (user,))
                        print("Grants granted for establishment")
                        db.cursor.execute("SELECT id FROM login WHERE name = %s", (user, ))
                        pop = db.cursor.fetchone()
                        db.cursor.execute("INSERT INTO restaurants (user_id, name) VALUES (%s, %s)", (pop, user))
                        #never happens because no commit, commit crashes the program?
                        db.cursor.execute("SELECT * FROM restaurants WHERE user_id = %s", (pop,))
                        restaurant = db.cursor.fetchone()
                        db.close()
                        db.change(user, stored_hashed_password)
                        db.connect()
                        return redirect(url_for('editrestaurant'))
                    else:
                        print("Unknown user type")
                    db.cursor.execute("FLUSH PRIVILEGES;")
                    "Connects the login user to the database"
                    print("Login successful 0")
                    db.close()
                    db.change(user, stored_hashed_password )
                    db.connect()

                    print("Login successful 1")

                    return render_template('mainpage.html')
                else:
                    print("Incorrect password")
                    return render_template('signin.html', error="Incorrect password")
            else:
                print("Invalid username or password")
                return render_template('startingPage.html')

        except MySQLdb.Error as e:
            print(f"An error occurred: {e}")
            return render_template('signin.html')

    elif (request.method == 'GET'):
        return render_template('signin.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():

    db.close()
    db.change("root", rootpswd)
    db.connect()

    if request.method == 'POST':
        newUser = request.form['newUserNameOrEmail']
        passWrd = request.form['newUserPassword']
        accType = request.form['accountType']

        print(newUser)
        print(passWrd)
        print(accType)
        try:
            db.cursor.execute("SELECT * FROM login WHERE EXISTS (SELECT * FROM login WHERE name = %s)", (newUser,))
            result = db.cursor.fetchone()
            if result:
                print("Username already exists")
                return render_template('signup.html')
            else:
                hashed_password = bcrypt.hashpw(passWrd.encode('utf-8'), bcrypt.gensalt())
                create_user_query = "CREATE USER IF NOT EXISTS %s@'localhost' IDENTIFIED BY %s;"
                db.cursor.execute(create_user_query, (newUser,  hashed_password))
                grant_user_query = "GRANT 'customer_user' TO %s@'localhost';"
                db.cursor.execute("FLUSH PRIVILEGES;")
                grant_restaurant_query = "GRANT 'restaurant_user' TO %s@'localhost';"

                db.cursor.execute("INSERT INTO login (name, password, type) VALUES (%s, %s, %s)",
                               (newUser,  hashed_password, accType))

                if accType == "User":
                    db.cursor.execute(grant_user_query, (newUser,))
                    db.cursor.execute("FLUSH PRIVILEGES;")
                    db.cursor.execute("SET ROLE 'customer_user'")

                else:
                    db.cursor.execute(grant_restaurant_query, (newUser,))
                    db.cursor.execute("FLUSH PRIVILEGES;")
                    db.cursor.execute("SET ROLE 'restaurant_user'")

            # Add the new user to the database session

            print("Added to the database")
            db.commit()


        except MySQLdb.Error as e:
            db.rollback()
            print(f"An error occurred: {e}")
        finally:
            return render_template('signup.html')

    else:
        return render_template('signup.html')


@app.route('/mainpage')
def mainpage():
    return render_template('mainpage.html')


@app.route('/loadNext')
def loadNext():
    global currentID
    default = ['Not available', '', '', '']
    valid = False
    userID = 1

    db.cursor.execute("SELECT MAX(id) FROM restaurants")
    maxID = db.cursor.fetchone()[0]
    print(f'The largest ID was {maxID}')
    i = 0
    try:
        while not valid and i < 50:
                if currentID <= maxID:  
                    print(f'i = {i}')
                    i += 1
                    print(f'\nCurrentID = {currentID}\n')
                    
                    db.cursor.execute("""SELECT name, cuisine_type, estabImg, restaurants.id FROM restaurants  LEFT JOIN liked_restaurants lr ON restaurants.id = lr.restaurant_id AND lr.user_id = %s WHERE restaurants.id = %s AND lr.restaurant_id IS NULL """, (userID, currentID))
                    
                    restaurant = db.cursor.fetchone()
                    currentID += 1

                    if restaurant is not None:
                        valid = True

                        for r in restaurant:
                            print(r)
                else:
                    currentID = 0

        restjson = {'name': restaurant[0],
                'cuisine_type': restaurant[1],
                'estabImg' : restaurant[2],
                'id' : restaurant[3]
                }
    except Exception as e:
            print(e)
            restjson = {'name': default[0],
                        'cuisine_type': default[1],
                        'estabImg' : default[2],
                        'id' : default[3]
                        }
    
    return jsonify(restjson)

@app.route('/addClicked', methods = ['POST','GET'])
def addLiked():
    if request.method == 'POST':
        try:
            user_id = 2  # Replace with the actual user ID from session or request
            restaurant_id = request.json.get('id')
            
            if not restaurant_id:
                return "Failed to get restaurant ID"

            db.cursor.execute("INSERT INTO liked_restaurants (user_id, restaurant_id) VALUES (%s, %s)", (user_id, restaurant_id))
            
            query = """
                INSERT INTO liked_restaurants (user_id, restaurant_id)
                VALUES (%s, %s)
            """
            db.cursor.execute(query, (user_id, restaurant_id))
            
            db.commit()

        except MySQLdb.Error as e:
            db.rollback()
            return 'operation unsuccessful'
        return 'operation succeeded'


@app.route('/userMenuView', methods=['POST', 'GET'])
def showMenu():

    try:
        print("Error here? 1")
        currID = 1
        print("Error here? 2")
        db.cursor.execute('SELECT id, name, description, price FROM menu_items WHERE restaurant_id = %s', (currID,))
        print("Error here? 3")
        rows = db.cursor.fetchall()
        
        for row in rows:
            for part in row:
                print(part)
        
        print("About to display info!")
        return render_template('userMenuView.html', rows = rows)

    except MySQLdb.Error as e:
        print(f"An error occurred: {e}")
        return render_template('userMenuView.html')



@app.route('/addfooditem', methods=['GET', 'POST'])
def addfooditem():
    if request.method == 'POST':
        # Retrieve form data
        db.cursor.execute("SELECT CURRENT_USER()")
        result = db.cursor.fetchone()
        #makes result able to be split
        results = ''.join(result)
        #for some reason helped it actually recognize a string?
        resultss = results
        # Parse the username (everything before '@')
        name = resultss.split('@')[0]
        db.cursor.execute("SELECT id FROM login WHERE name = %s", (name,))
        I = db.cursor.fetchone()
        # Fetch restaurant details from the database
        db.cursor.execute("SELECT id FROM restaurants WHERE user_id = %s", (I,))
        theid = db.cursor.fetchone()
        # where i found that restaurants never were created
        print(theid)
        restaurant_id = theid
        food_name = request.form['food-name']
        food_description = request.form['food-description']
        food_price = request.form['food-price']
        food_url = request.form['food-url']

        try:
            # Insert food item into menu_items table
            db.cursor.execute("INSERT INTO menu_items (restaurant_id, name, foodurl, description, price)VALUES (%s, %s, %s, %s, %s)", 
                           (restaurant_id, food_name, food_url, food_description, food_price))
            db.commit()
            print("Food item added successfully")
            return redirect(url_for('editrestaurant'))
            #throws an error?
            #return render_template('addfooditem.html', message="Food item added successfully")
        except MySQLdb.Error as e:
            #db.rollback()
            print(f"An error occurred: {e}")
            return redirect(url_for('editrestaurant'))
            #return render_template('addfooditem.html', error="Failed to add food item. Please try again.")
    return render_template('addfooditem.html')

@app.route('/editrestaurant', methods=['GET', 'POST'])
def editrestaurant():
    if request.method == 'GET':
        try:
            db.cursor.execute("SELECT CURRENT_USER()")
            result = db.cursor.fetchone()
            results = ' '.join(str(item) for item in result)
            resultss = results
            # Parse the username (everything before '@')
            name = resultss.split('@')[0]
            db.cursor.execute("SELECT id FROM login WHERE name = %s", (name,))
            I = db.cursor.fetchone()
            # Fetch restaurant details from the database
            db.cursor.execute("SELECT user_id FROM restaurants WHERE user_id = %s", (I,))
            restaurant_id = db.cursor.fetchone()

            # Fetch restaurant details using fetched restaurant_id
            db.cursor.execute("SELECT * FROM restaurants WHERE id = %s", (restaurant_id,))
            restaurant = db.cursor.fetchone()
            current_url = request.path
            if current_url == '/editrestaurant':
                return render_template('editrestaurant.html', restaurant=restaurant)
            else: 
                return redirect(url_for('editrestaurant'))
            
        except MySQLdb.Error as e:
            print(f"An error occurred: {e}")
            return render_template('editrestaurant.html', error="Failed to fetch restaurant details.")
    
    elif request.method == 'POST':
        # Similar to GET method, fetch and update restaurant details
        try:
            db.cursor.execute("SELECT CURRENT_USER()")
            result = db.cursor.fetchone()
            results = ''.join(result)
            resultss = results
            # Parse the username (everything before '@')
            name = resultss.split('@')[0]
            db.cursor.execute("SELECT id FROM login WHERE name = %s", (name,))
            I = db.cursor.fetchone()
            # Fetch restaurant details from the database
            db.cursor.execute("SELECT user_id FROM restaurants WHERE user_id = %s", (I,))
            restaurant_id = db.cursor.fetchone()

            # AAttempts to get the restaurant
            db.cursor.execute("SELECT * FROM restaurants WHERE id = %s", (restaurant_id,))
            restaurant = db.cursor.fetchone()

            if restaurant:
                # Retrieve new data
                restaurant_title = request.form['restaurant-title']
                restaurant_description = request.form['restaurant-description']
                restaurant_address = request.form['restaurant-address']
                restaurant_state = request.form['restaurant-state']
                restaurant_city = request.form['restaurant-city']
                restaurant_zip = request.form['restaurant-zip']
                restaurant_country = request.form['restaurant-country']
                restaurant_phone = request.form['restaurant-phone']
                restaurant_website = request.form['restaurant-website']
                restaurant_openhours = request.form['restaurant-openhours']
                restaurant_closehours = request.form['restaurant-closehours']

                # Update restaurant details in the database
                db.cursor.execute("""
                    UPDATE restaurants 
                    SET name = %s, description = %s, address = %s, state = %s, city = %s, postal_code = %s,
                        country = %s, phone_number = %s, website = %s, opening_hours = %s, closing_hours = %s
                    WHERE id = %s
                """, (restaurant_title, restaurant_description, restaurant_address, restaurant_state,
                      restaurant_city, restaurant_zip, restaurant_country, restaurant_phone,
                      restaurant_website, restaurant_openhours, restaurant_closehours, restaurant_id))
                db.commit()
                print("Restaurant details updated successfully")
                return redirect(url_for('editrestaurant'))
            else:
                return redirect(url_for('editrestaurant'))
            
        except MySQLdb.Error as e:
            db.rollback()
            print(f"An error occurred: {e}")
            return redirect(url_for('editrestaurant'))
            
@app.route('/edituser', methods=['GET', 'POST'])
def edit_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        city = request.form['city']
        state = request.form['state']
        postal_code = request.form['postal_code']
        country = request.form['country']

        login_id = ""

        db.cursor.execute("""
            UPDATE customer
            SET first_name=%s, last_name=%s, phone_number=%s, city=%s, state=%s, postal_code=%s, country=%s
            WHERE login_id=%s
        """, (first_name, last_name, phone_number, city, state, postal_code, country, login_id))
        
        db.commit()
        return redirect(url_for('mainpage'))  

if __name__ == '__main__':
    app.run(debug=True)
