import MySQLdb
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)

currentID = 0

# Database connection parameters
host = "localhost"
user = "root"
password = "[EveryGoodHorseEats99Carrots]"
database = "Foodie"

db = MySQLdb.connect(host=host, user=user, passwd=password, db=database)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('mainpage.html')

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
                "Shows the grants for each user"
                show_grants_query = "SHOW GRANTS FOR %s@'localhost' USING 'customer_user';"
                cursor.execute(show_grants_query, (user,))
                privileges = cursor.fetchall()

                for privilege in privileges:
                    print(privilege)
                    "manually input the privileges  "
                
                #TESTING HERE
                cursor.execute("GRANT 'customer_user' TO %s@'localhost';", (user,))

                cursor.execute("FLUSH PRIVILEGES;")
                "Connects the login user to the database"
                print("Login successful 0")
                

                newDB = MySQLdb.connect(host="localhost", user=user, passwd=passWrd, db=database)
                print("Login successful 1")
                
                newCursor = newDB.cursor()
                print("Login successful 2")

                #newDb.close()
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
            cursor.execute("SELECT * FROM login WHERE EXISTS (SELECT * FROM login WHERE name = %s)", (newUser,))
            result = cursor.fetchone()
            if result:
                print("Username already exists")
                return render_template('signup.html')
            else:
                create_user_query = "CREATE USER IF NOT EXISTS %s@'localhost' IDENTIFIED BY %s;"
                cursor.execute(create_user_query, (newUser, passWrd))
                grant_user_query = "GRANT 'customer_user' TO %s@'localhost';"
                cursor.execute("FLUSH PRIVILEGES;")
                grant_restaurant_query = "GRANT 'restaurant_user' TO %s@'localhost';"

                cursor.execute("INSERT INTO login (name, password, type) VALUES (%s, %s, %s)",
                               (newUser, passWrd, accType))

                if accType == "User":
                    cursor.execute(grant_user_query, (newUser,))
                    cursor.execute("FLUSH PRIVILEGES;")
                    cursor.execute("SET ROLE customer_user")

                else:
                    cursor.execute(grant_restaurant_query, (newUser,))
                    cursor.execute("FLUSH PRIVILEGES;")
                    cursor.execute("SET ROLE restaurant_user")
                    

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

    cursor.execute("SELECT MAX(id) FROM restaurants")
    maxID = cursor.fetchone()[0]
    print(f'The largest ID was {maxID}')
    i = 0
    try:
        while not valid and i < 50:
                if currentID <= maxID:  
                    print(f'i = {i}')
                    i += 1
                    print(f'\nCurrentID = {currentID}\n')
                    
                    cursor.execute("""SELECT name, cuisine_type, estabImg, restaurants.id FROM restaurants  LEFT JOIN liked_restaurants lr ON restaurants.id = lr.restaurant_id AND lr.user_id = %s WHERE restaurants.id = %s AND lr.restaurant_id IS NULL """, (userID, currentID))
                    
                    restaurant = cursor.fetchone()
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
                print('\Operation to add liked restaurant failed.\n')
                return "Failed to get restaurant ID"

            cursor.execute("INSERT INTO liked_restaurants (user_id, restaurant_id) VALUES (%s, %s)", (user_id, restaurant_id))
            db.commit()

        except MySQLdb.Error as e:
            db.rollback()
            return 'operation unsuccessful'
        return 'operation succeeded'

@app.route('/userMenuView', methods = ['POST', 'GET'])
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

if __name__ == '__main__':
    app.run(debug=True)
