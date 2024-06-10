import MySQLdb
from flask import Flask, render_template, request

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
