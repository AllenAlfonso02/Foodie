# Foodie
A scalable restaurant pairing application with role-based access 

## Problem
Our application provides assitance in the decision making process of which restaurant to go to. A common problem that is widely answered with "I dont know".

## Dependencies
Local mysql instance

python 3.x or above

python modules:
- MySQLdb
- flask

## Setup
1. Clone the repo
2. Install dependencies
> pip install Flask mysqlclient
3. Enter your mysql root 
password in `setup.py` , `app.py` , `populate.py`
4. Run the setup file:
> python3 setup.py
5. To test with sample data (optional):
> python3 populate.py

## Running the app
1. Start the app
> python3 app.py
2. Go to [This URL][localhostURL], which can also be found when the server is launched

[localhostURL]: http://127.0.0.1:5000/

## Separation of work

Alex: Add Food Item and Edit Restaurant (Front-end & Back-end).
Allen: User Menu Page, SignIn, Signup, and Starting Page (Front-end & Back-end) and Roles
Julie: Mainuser page (Front-end & Back-end) and populate.py. 
Kester: Database and Roles (Back-end)
Nathan: Database and userSettings page (Front-end & Back-end)
Wesley: likedRestaurant page (Front-end & Back-end)
