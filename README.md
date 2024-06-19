# Foodie
A scalable restaurant pairing application with role-based access 

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
password in `setup.py` , `app.py` , `setup.py`
4. Run the setup file:
> python3 setup.py
5. To test with sample data (optional):
> python3 populate.py

## Running the app
1. Start the app
> python3 app.py
2. Go to [This URL][localhostURL], which can also be found when the server is launched

[localhostURL]: http://127.0.0.1:5000/