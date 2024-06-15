import MySQLdb
from flask import Flask, render_template, request

app = Flask(__name__)

# Database connection parameters
host = "localhost"
user = "root"
password = "septons"
database = "foodie"

db = MySQLdb.connect(host=host, user=user, passwd=password, db=database)
cursor = db.cursor()


@app.route('/')
def home():
    return render_template('startingPage.html')


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    print("in here?")
    if request.method == 'POST':

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
                grant = [
                    "GRANT SELECT ON Foodie.restaurants TO %s@'localhost';",
                    "GRANT SELECT ON Foodie.menu_items TO %s@'localhost';",
                    "GRANT SELECT, INSERT, UPDATE ON Foodie.customer TO %s@'localhost';"
                ]
                for command in grant:
                    cursor.execute(command, (user,))
                ###cursor.execute(grant, (user, ))

                print("Login successful")
                cursor.execute("FLUSH PRIVILEGES;")
                "Connects the login user to the database"
                newDB = MySQLdb.connect(host="localhost", user=user, passwd=passWrd, db=database)
                newCursor = newDB.cursor()

            else:
                print("Invalid username or password")

            return render_template('mainpage.html')


        except MySQLdb.Error as e:
            print(f"An error occurred: {e}")
            return render_template('singin.html')

    elif (request.method == 'GET'):
        print("in here? 6")
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


                else:
                    cursor.execute(grant_restaurant_query, (newUser,))
                    cursor.execute("FLUSH PRIVILEGES;")

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


if __name__ == '__main__':
    app.run(debug=True)
