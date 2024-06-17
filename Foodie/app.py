import MySQLdb
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Database connection parameters
host = "localhost"
user = "root"
password = ""
database = "Foodie"

db = MySQLdb.connect(host=host, user=user, passwd=password, db=database)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('startingPage.html')


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    print("in here?")
    if (request.method == 'POST'):

        user = request.form['userNameOrEmail']
        passWrd = request.form['userPassword']

        print(user)
        print(passWrd)

        try:

            cursor.execute("SELECT * FROM login WHERE EXISTS (SELECT * FROM login WHERE name = %s AND password = %s)",
                           (user, passWrd))
            result = cursor.fetchone()

            if result:
                print("Login successful")
                return render_template('mainpage.html')
            else:
                print("Invalid username or password")
                return render_template('startingPage.html')


        except MySQLdb.Error as e:
            print(f"An error occurred: {e}")
            return render_template('singin.html')

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
            cursor.execute("INSERT INTO login (name, password, type) VALUES (%s, %s, %s)",
                           (newUser, passWrd, accType))
            print("Added to the database")
            db.commit()
            cursor.execute("INSERT INTO customer (username, password) VALUES (newUser, passWrd)")
            db.commit()
            cursor.execute("SELECT id FROM customer WHERE username = %s", (newUser,))
            customer_id = cursor.fetchone()
            if accType == 'Establishment':
                cursor.execute("INSERT INTO restaraunts (user_id) VALUES (%s)", (customer_id,))
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
    global currentID; currentID += 1
    testjson = {"picture" : "https://www.connarchitects.com/wp-content/uploads/2019/09/CONN_Edison-2.jpg",
                "name" : "Dummy Restaurant",
                "description" : "This is a json created to test my restaurant.fdhfkjsdhfjdshfkhdskfhkjfsdhjdfhksfhjkhsfkdhfds",
                }
    return jsonify(testjson)

@app.route('/addCliked', methods = ['POST', 'GET'])
def addLiked():
    if request.method == 'POST':
        try:
            #Insert liked restaurant
            cursor.execute()
            db.commit()
        except:
            db.rollback()
            return "Unsuccessful insert operation."
        finally:
            db.close()
            return "Successfully added Restaurant"

@app.route('/addfooditem', methods=['POST'])
def addfooditem():
    if request.method == 'POST':
        # Retrieve form data
        restaurant_id = request.form['restaurant_id'] 
        food_name = request.form['food-name']
        food_description = request.form['food-description']
        food_price = request.form['food-price']
        food_url = request.form['food-url']

        try:
            # Insert food item into menu_items table
            cursor.execute("""
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
def edit_restaurant(restaurant_id):
    if request.method == 'GET':
        try:
            # Fetch restaurant details from the database
            cursor.execute("SELECT * FROM restaurants WHERE id = %s", (restaurant_id,))
            restaurant = cursor.fetchone()

            # Assuming restaurant is a dictionary-like object with keys like 'closing_hours'
            return render_template('editrestaurant.html', restaurant=restaurant)
        except MySQLdb.Error as e:
            print(f"An error occurred: {e}")
            return render_template('editrestaurant.html', error="Failed to fetch restaurant details.")
    
    elif request.method == 'POST':
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

        try:
            # Update restaurant details in the database
            cursor.execute("""
                UPDATE restaurants 
                SET name = %s, description = %s, address = %s, state = %s, city = %s, postal_code = %s,
                    country = %s, phone_number = %s, website = %s, opening_hours = %s, closing_hours = %s
                WHERE id = %s
            """, (restaurant_title, restaurant_description, restaurant_address, restaurant_state,
                  restaurant_city, restaurant_zip, restaurant_country, restaurant_phone,
                  restaurant_website, restaurant_openhours, restaurant_closehours, restaurant_id))
            db.commit()
            print("Restaurant details updated successfully")
            return redirect(url_for('editrestaurant', restaurant_id=restaurant_id))
        except MySQLdb.Error as e:
            db.rollback()
            print(f"An error occurred: {e}")
            return render_template('editrestaurant.html', error="Failed to update restaurant details.")


if __name__ == '__main__':
    app.run(debug=True)
