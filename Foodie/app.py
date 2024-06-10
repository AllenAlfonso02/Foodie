import MySQLdb
from flask import Flask, render_template, request
app = Flask(__name__)

# Database connection parameters
host = "localhost"
user = "root"
password = "0179849Aa$"

db = MySQLdb.connect(host=host, user=user, passwd=password)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('startingPage.html')

@app.route('/signin', methods = ['POST','GET'])
def signin():
    print("in here?")
    if (request.method == 'POST'):
        print("in here? 1")
        user = request.form['userNameOrEmail']
        passWrd = request.form['userPassword']

        print(user)
        print(passWrd)

        print("in here? 2")

        try:
            print("in here? 3")
            #existsQuerry = "SELECT * FROM login WHERE EXISTS (SELECT * FROM login WHERE name = ? AND password = ?)", (user,passWrd)
            #cursor.execute(existsQuerry, (user, passWrd))
            
            cursor.execute("SELECT * FROM login WHERE EXISTS (SELECT * FROM login WHERE name = ? AND password = ?)", (user, passWrd))
            print("in here? 4")
            return render_template('mainpage.html')

        except:
            print("in here? 5")
            return render_template('singin.html')

    elif (request.method == 'GET'):
        print("in here? 6")
        return render_template('signin.html')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if (request.method == 'POST'):
        user = request.form['newUserNameOrEmail']
        passWrd = request.form['newUserPassword']
        accType = request.form['accountType']

        print(user)
        print(passWrd)
        print(accType)

        try:
            cursor.execute("INSERT INTO login (name, password, type) VALUES (?,?,?)", (user, passWrd, accType))
            db.commit()

        except:
            db.rollback()
        finally:
            return render_template('signup.html')
    
    else:
        return render_template('signup.html')

@app.route('/mainpage')
def mainpage():
    return render_template('mainpage.html')

if __name__ == '__main__':
    app.run(debug = True)