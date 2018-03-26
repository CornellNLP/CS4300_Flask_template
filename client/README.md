# React-Flask BoilerPlate

Technologies involved include:
1. Flask
2. SQLAlchemy
3. Marshmallow
4. MySQL
5. React
6. React-Router
7. Redux

## Setting Up Database
Ensure you have `mysql` plus command line tools setup:
````bash
mysql
mysql> CREATE DATABASE my_db_name;
mysql> \q
cd src
python manage.py db init  
python manage.py db migrate
python manage.py db upgrade
````

## Environment Variables
I highly recommend [`autoenv`](https://github.com/kennethreitz/autoenv).
The required environment variables for this API are the following:

````bash
export DB_USERNAME=CHANGE_ME
export DB_PASSWORD=CHANGE_ME
export DB_HOST=localhost
export DB_NAME=my_db_name
export APP_SETTINGS=config.CHANGE_ME
````
