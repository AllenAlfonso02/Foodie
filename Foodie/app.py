import MySQLdb
from flask import Flask, render_template, request, jsonify, redirect, url_for
import MySQLdb.cursors

app = Flask(__name__)

currentID = 0


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


db = mySQLClass("localhost", "root", "septons")
db.connect()


@app.route('/')
def home():
    return render_template('startingPage.html')


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    print("in here?")
    db.close()
    db.change("root", "septons")
    db.connect()
    if (request.method == 'POST'):

        user = request.form['userNameOrEmail']
        passWrd = request.form['userPassword']

        print(user)
        print(passWrd)

        try:

            db.cursor.execute("SELECT * FROM login WHERE EXISTS (SELECT * FROM login WHERE name = %s AND password = %s)",
                           (user, passWrd))
            result = db.cursor.fetchone()

            if result:
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
                    db.cursor.execute("SELECT * FROM restaurants WHERE id = %s", (user,))
                    print("1")
                    restaurant = db.cursor.fetchone()
                    return render_template('editrestaurant.html', restaurant=restaurant)
                else:
                    print("Unknown user type")
                db.cursor.execute("FLUSH PRIVILEGES;")
                "Connects the login user to the database"
                print("Login successful 0")
                db.close()
                db.change(user, passWrd)
                db.connect()

                print("Login successful 1")

                print("Login successful 2")


                return render_template('mainpage.html')
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
                create_user_query = "CREATE USER IF NOT EXISTS %s@'localhost' IDENTIFIED BY %s;"
                db.cursor.execute(create_user_query, (newUser, passWrd))
                grant_user_query = "GRANT 'customer_user' TO %s@'localhost';"
                db.cursor.execute("FLUSH PRIVILEGES;")
                grant_restaurant_query = "GRANT 'restaurant_user' TO %s@'localhost';"

                db.cursor.execute("INSERT INTO login (name, password, type) VALUES (%s, %s, %s)",
                               (newUser, passWrd, accType))

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
    #select statement
    global currentID;
    currentID += 1
    testjson = {"picture": "https://www.connarchitects.com/wp-content/uploads/2019/09/CONN_Edison-2.jpg",
                "name": "Dummy Restaurant",
                "description": "This is a json created to test my restaurant.fdhfkjsdhfjdshfkhdskfhkjfsdhjdfhksfhjkhsfkdhfds",
                }
    return jsonify(testjson)


@app.route('/addClicked', methods=['POST'])
def addLiked():
    if request.method == 'POST':
        try:
            user_id = 1  # Replace with the actual user ID from session or request
            restaurant_id = request.json.get('restaurant_id')

            if not restaurant_id:
                return "Failed to get restaurant ID"

            query = """
                INSERT INTO liked_restaurants (user_id, restaurant_id)
                VALUES (%s, %s)
            """
            cursor.execute(query, (user_id, restaurant_id))
            db.commit()

            return "Successfully added Restaurant"
        except MySQLdb.Error as e:
            db.rollback()
            return "Unsuccessful insert operation"


@app.route('/userMenuView', methods=['POST', 'GET'])
def showMenu():
    if (request.method == 'GET'):
        try:
            db.row_factory = MySQLdb.Row

            currID = ""

            cursor.execute('SELECT * FROM menu_items WHERE restaurant_id = ?', (currID,))

            rows = cursor.fetchall()

        except:
            return render_template('userMenuView.html')

    else:
        return render_template('startingPage.html')

@app.route('/addfooditem', methods=['POST'])
def addfooditem():
    if request.method == 'POST':
        # Retrieve form data
        cursor.execute("SELECT CURRENT_USER()")
        result = cursor.fetchone()
        # Parse the username (everything before '@')
        name = result.split('@')[0]
        cursor.execute("SELECT id FROM login WHERE name = %s", (name,))
        I = cursor.fetchone()
        # Fetch restaurant details from the database
        cursor.execute("SELECT id FROM restaurants WHERE user_id = %s", (I,))
        theid = cursor.fetchone()
        restaurant_id = theid
        food_name = request.form['food-name']
        food_description = request.form['food-description']
        food_price = request.form['food-price']
        food_url = request.form['food-url']

        try:
            # Insert food item into menu_items table
            db.cursor.execute("""
                INSERT INTO menu_items (restaurant_id, name, foodurl, description, price)
                VALUES (%s, %s, %s, %s, %s)
            """, (restaurant_id, food_name, food_url, food_description, food_price))
            db.commit()
            print("Food item added successfully")
            return render_template('addfooditem.html', message="Food item added successfully")
        except MySQLdb.Error as e:
            db.rollback()
            print(f"An error occurred: {e}")
            return render_template('addfooditem.html', error="Failed to add food item. Please try again.")
    return render_template('addfooditem.html')

@app.route('/editrestaurant', methods=['GET', 'POST'])
def edit_restaurant():
    if request.method == 'GET':
        try:
            db.cursor.execute("SELECT CURRENT_USER()")
            result = db.cursor.fetchone()
            # Parse the username (everything before '@')
            name = result.split('@')[0]
            db.cursor.execute("SELECT id FROM login WHERE name = %s", (name,))
            I = db.cursor.fetchone()
            # Fetch restaurant details from the database
            db.cursor.execute("SELECT user_id FROM restaurants WHERE user_id = %s", (I,))
            restaurant_id = cursor.fetchone()

            # Fetch restaurant details using fetched restaurant_id
            db.cursor.execute("SELECT * FROM restaurants WHERE id = %s", (restaurant_id,))
            restaurant = db.cursor.fetchone()

            if restaurant:
                return render_template('editrestaurant.html', restaurant=restaurant)
            else:
                return render_template('editrestaurant.html', error="Restaurant not found.")
            
        except MySQLdb.Error as e:
            print(f"An error occurred: {e}")
            return render_template('editrestaurant.html', error="Failed to fetch restaurant details.")
    
    elif request.method == 'POST':
        # Similar to GET method, fetch and update restaurant details
        try:
            db.cursor.execute("SELECT CURRENT_USER()")
            result = db.cursor.fetchone()
            # Parse the username (everything before '@')
            name = result.split('@')[0]
            db.cursor.execute("SELECT id FROM login WHERE name = %s", (name,))
            I = db.cursor.fetchone()
            # Fetch restaurant details from the database
            db.cursor.execute("SELECT user_id FROM restaurants WHERE user_id = %s", (I,))
            restaurant_id = db.cursor.fetchone()

            # Assuming 'restaurant_id' is the correct identifier for your restaurant
            db.cursor.execute("SELECT * FROM restaurants WHERE id = %s", (restaurant_id,))
            restaurant = db.cursor.fetchone()

            if restaurant:
                # Retrieve updated form data
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
                return render_template('editrestaurant.html', error="Restaurant not found.")
            
        except MySQLdb.Error as e:
            db.rollback()
            print(f"An error occurred: {e}")
            return render_template('editrestaurant.html', error="Failed to update restaurant details.")
            
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
