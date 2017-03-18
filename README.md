# CS4300 - Flask Template
## Notes
Are you one who enjoys Ruby on Rails or the MVC structure for backend-design, well this template-based Flask app is just for you :)
Because this class heavily relies on python libraries it was decided to write the app in Python for your convinence. If you have any questions dont hesistate to ask the TAs or come to OH. In this README I will include an overview section with information on the flask app architecture and a step-by-step guide to loading up your app in dev and production (in Heroku) with EC2/EB coming soon. This README was written by Ilan Filonenko with help from Joseph Antonakakis: **SHAMELESS PLUG:** If this type of work interests you, make sure to check out the course, **Principles of Backend Engineering**, which will be co-taught by Ilan and Joe next semester under CS 1998, covering backend engineering, database design, dev ops, and scalable system architecture.
## Table of Contents
### [Overview](#overview-of-the-project-and-introduction-to-flask)
### [Step-By-Step](#step-by-step-guide)
## Overview of the project and Introduction to Flask
This will overview `Flask` development operations for setting up a new project with an emphasis on the `Model-View-Controller` design pattern.

This guide will be utilizing `PostgreSQL` to drive persistent storage on the backend.  

### Get PyPI

This guide depends on you being able to easily download Python modules.  In order to do so, you should get `PyPI`.  Follow the basic guide [here](https://pip.pypa.io/en/stable/installing/).

### Virtualenv - The Key to Python Projects

Before even touching `Flask`, you should be introduced into `virtualenv` (if you have not already seen this amazing tool). `Virtualenv` allows you to create an isolated environment to build and run a Python project in.  All dependencies for the project can be freshly declared and utilized, and the project can, therefore, be built and executed in a modular and isolated fashion.  In addition, if you download a preexisting Python project, you can create a virtual environment with `virtualenv` to install and store all dependencies for the project.  Think of it like your `node_modules` file if you come from `Node.js`, or your project gems if you come from `Ruby on Rails`.  To install, go [here](https://virtualenv.pypa.io/en/stable/installation/).  For dead-simple usage, go [here](https://virtualenv.pypa.io/en/stable/userguide/).

Once you have `virtualenv` setup, create an actual virtual environment with the following command:

```bash
virtualenv venv
```

In the above example, I chose to name the environment `venv`, but you can name it whatever you'd like.

To activate and enter the virtual environment, run the following:

```bash
source venv/bin/activate
```

The following command line prompt will indicate that you're in the virtual environment:

```bash
(venv) >
```

To deactivate the virtual environment, run the following:

```bash
deactivate
```

I have inluded a requirements.txt file in the project. The typical workflow will be to install something via `pip`, (whatever you want) and then run the following:

```bash
pip freeze > requirements.txt
```

The command `pip freeze` actually lists the dependencies encapsulated by the virtual environment.  The above command copies those into a text file that will allow one to run the following on downloading and using the Python project:

```bash
pip install -r requirements.txt
```

**NOTE**: The `.env` file is intentionally **NOT** `.gitignore`-ed.  

### Flask App
#### Organization
A `Flask` app has some utility scripts at the top-level, and has a modular organization when defining any sort of functionality.  Dividing up a `Flask` app into modules allows one to separate resource / logic concerns.  

The utility scripts at the top level include the following:

```bash
config.py # describes different environments that app runs in
manage.py # holds functionality for migrating your database (changing its schema)
run.py    # runs the app on a port
```

The entire functional backend of a `Flask` app is housed in a parent module called `app`.  You can create this by creating a directory `app` and populating it with an `__init__.py` file.  Then, inside that `app` directory, you can create modules that describe the resources of your app.  These modules should be as de-coupled and reusable as possible.  For example, let's say I need a bunch of user authentication logic described by a couple of endpoints and helper functions.  These might be useful in another `Flask` app and can be comfortably separated from other functionality.  As a result, I would make a module called `accounts` inside my app directory.  Each module (including `app`) should also have a `templates` directory if you plan on adding any `HTML` views to your app.   

#### Template
The use of templates here is specifically for the purpose of mimicing the structure of an MVC application. In this application I have seperated the system into two seperate templates: accounts and irsystem, since some of you might need to leverage the database for user/session log flow so you would only use the irsystem template. The irsystem is what you will be manipulating for the purposes of your information retrevial. If you look at the file `search_controller.py` you can see that we are rendering the view with data being passed in. This data will the results from your IR system which you will customize accordingly. You may make more models/controllers for organization purposes. 

### Database Setup

In this example, as stated, `PostgreSQL` (or `Postgres`) will be the database leveraged.  `Postgres` can be installed a multitude of ways, but if you're on `OSX` I recommend utilizing the [`Postgres App`](https://postgresapp.com/).  

Once you have `Postgres` setup and have your `$PATH` configured accordingly, run the following:

```bash
# Enter postgres command line interface
$ psql
# Create your database
CREATE DATABASE my_app_db;
# Quit out
\q
```

The above creates the actual database that will be used for this application and the name of the database is `my_app_db` which you can change, but make sure to change the .env and in your production app accordingly which I will talk about lower in this guide. 

Rather than writing raw-SQL for this application, I have chosen to utilize [`SQLAlchemy`](http://flask-sqlalchemy.pocoo.org/2.1/) (specifically, `Flask-SQLAlchemy`) as a database `Object-Relational-Model` (`ORM`, for short).  In addition, for the purposes of serialization (turning these database entities into organized [`JSONs`](http://www.json.org/) that we can send over the wire) and deserialization (turning a `JSON` into a entity once again), I have chosen to use [`Marshmallow`](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/) (specifically, `marshmallow-SQLAlchemy`).

Several modules are needed to completely integrate `Postgres` into a `Flask` app, but several of these modules are co-dependent on one another. I have included all of these in the requirements.txt file, these modules include: flask-migrate marshmallow-sqlalchemy psycopg2.

The migration script, `manage.py`  will be used to capture changes you make over time to the schemas of your various models.  
This script will not work out of the gate and refers to components we have not yet defined in our app, but I will describe these below:

```python
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
  manager.run()
```
In the above, `app` refers to the module we created above in the **File Organization** section.  `db` refers to our reference to the database connection that we have yet to define in the `app` module.  

This script can be used in the following way to migrate your database, on changing your models:
``` bash
# Initialize migrations
python manage.py db init
# Create a migration
python manage.py db migrate
# Apply it to the DB
python manage.py db upgrade
```
You should run these methods after having the .env setup because it requires the APP_SETTINGS and DATABASE_URL to be defined. If you get errors in this section as a result of key-errors for APP_SETTINGS and DATABASE_URL go to the **Environmental Variables** section and make sure to delete the migrations folder that is already created with running `python manage.py db init`

### Configuration Setup
Now that we have setup our database and have handled our `manage.py` script, we can create our `config.py` script, which involves the database and various other configuration information specific to `Flask`.  This file will be used in our initialization of the `Flask` app in the `app` module in the near future.  

An example of a `config.py` file that is used in the project looks like this:

``` python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Different environments for the app to run in

class Config(object):
  DEBUG = False
  CSRF_ENABLED = True
  CSRF_SESSION_KEY = "secret"
  SECRET_KEY = "not_this"
  SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class ProductionConfig(Config):
  DEBUG = False

class StagingConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class DevelopmentConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class TestingConfig(Config):
  TESTING = True
```

The above defines several classes used to instantiate configuration objects in the creation of a `Flask` app.  Let's go through some of the variables:

* `DEBUG` indicates whether or not debug stack traces will be logged by the server.
* `CSRF_ENABLED`, `CSRF_SESSION_KEY`, and `SECRET_KEY` all relate to `Cross-Site-Request-Forgery`, which you can read more about [here](https://goo.gl/qkGU9).  
* `SQLALCHEMY_DATABASE_URI` refers to the database URL (a server running your database).  In the above example, I refer to an environment variable `'DATABASE_URL'`.  I will be discussing environment variables in the next section, so stay tuned.

### Environmental Variables
Environment variables allow one to specify credentials like a sensitive database URL, API keys, secret keys, etc.  These variables can be manually `export-ed` in the shell that you are running your server in, but that is a clunky approach.  The tool [`autoenv`](https://github.com/kennethreitz/autoenv) solves this problem.  

`autoenv` allows for environment variable loading on `cd`-ing into the base directory of the project. Follow the following command line arguments to install `autoenv`:

``` bash
# Install the package from pip
pip install autoenv
# Override cd by adding this to your .?rc file (? = bash, zsh, fish, etc), I'll use
echo "source `which activate`" >> ~/.?rc
# Reload your shell
source ~/.?rc
# Make a .env file to hold variables
touch .env
```

As mentioned in the above code, your `.env` file will be where you hold variables, and will look something like this:

``` bash
# Set the environment type of the app (see config.py)
export APP_SETTINGS=config.DevelopmentConfig
# Set the DB url to a local database for development
export DATABASE_URL=postgresql://localhost/my_app_db
````

As you can see above in the example, I reference a specific configuration class (`DevelopmentConfig`), meaning I plan on working in my development environment.  I also have my database URL. Both of which are used heavily in the app. In local mode you will be maniuplating the .env file but in production you will be manipulating the Config Variables in your Heroku instance or you will modify the .env files in your AWS EC2/EB application.

**NOTE:**  Be sure to `gitignore` your `.env` file.  

### Flask App Setup

Up until now, we haven't been able to run our server. 

The configurations of the `Flask` app are contained in `./app/__init__.py`.  The file should look like this:

``` python
# Gevent needed for sockets
from gevent import monkey
monkey.patch_all()

# Imports
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

# Configure app
socketio = SocketIO()
app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# DB
db = SQLAlchemy(app)

# Import + Register Blueprints
# WORKFLOW:
# from app.blue import blue as blue_print
# app.register_blueprint(blue_print)

# Initialize app w/SocketIO
socketio.init_app(app)

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
  return render_template("404.html"), 404
```

Let's unpack this file piece by piece.  The top initializes `Gevent`, [a coroutine-based Python networking library](http://www.gevent.org/) for `Socket.IO` (a very useful socket library useful in adding real-time sockets to your app).  The next section imports several libraries, initializes our `Flask` app, set our app up with the configurations from the appropriate `config.py` class, creates the `db` connection pool, bootstraps `Socket.IO` to our `Flask` app, and sets the `404` error page that the app should present on not finding a resource.  **NOTE**: the comments regarding registering a "blueprint" will be where we register our sub-modules with our main, parent `Flask` app.  

Since we have involved `Socket.IO` and `Gevent`, you wil see it in requirements.txt

Finally, in order to actually start our server, you will run the  `run.py` script.  This script can be placed at the root of our project:

``` python
from app import app, socketio

if __name__ == "__main__":
  print "Flask app running at http://0.0.0.0:5000"
  socketio.run(app, host="0.0.0.0", port=5000)

```


Now, at the root of your application, you can run:

``` bash
python run.py
```

Your server is now running!

**NOTE:** If you get issues regarding `APP_SETTINGS` or `DATABASE_URL`, you should ensure your `.env` is setup properly, and you should `cd` out of and back into your project root.

## That's it, for now...

This marks the end of project configuration for a well-constructed `Flask` app following `MVC`.  However, for additional development-related advice regarding project setup, keep reading.  

### Accounts Blueprint

Now we will be diving into writing `Models` and `Controllers` for an `accounts` blueprint that will serve as reusable `users-sessions` module that can be added to any application desiring a sign-up system.  We make some short-cuts along the way in order to increase this guide's brevity, while still providing meaningful sample code and explanations for the different components of the system.  

We must create our module within `app`, such that it contains the following structure:

``` bash
.
├── __init__.py
├── controllers
│   ├── __init__.py
│   ├── sessions_controller.py
│   └── users_controller.py
└── models
    ├── __init__.py
    ├── session.py
    └── user.py
``` 

Let's start with `./app/accounts/__init__.py`.  This file contains a couple of lines of information specifying the `Flask Blueprint` information of this module, as well import `controllers`:

``` python
from flask import Blueprint

# Define a Blueprint for this module (mchat)
accounts = Blueprint('accounts', __name__, url_prefix='/accounts')

# Import all controllers
from controllers.users_controller import *
from controllers.sessions_controller import *
````

In addition, register your new blueprint in `./app/__init__.py` by changing the lines:

``` python
# Import + Register Blueprints
# WORKFLOW:
# from app.blue import blue as blue_print
# app.register_blueprint(blue_print)
```

to:

``` python
# Import + Register Blueprints
from app.accounts import accounts as accounts
app.register_blueprint(accounts)
```

#### The Models

The models created will correspond, field-by-field, to the database tables that will be setup as a result of you running the series of migration commands listed above in the **Database Setup** section.

#### Base Model and Imports

Before looking into the `Base` model (the abstract model parent class that all models will extend from) we will look at Werkzeug, included in your requirements.txt, which is a module that is required to hash user-passwords ([you never want to store passwords in plain-text](https://arstechnica.com/security/2016/09/plaintext-passwords-and-wealth-of-other-data-for-6-6-million-people-go-public/)).  We should, technically, [salt](https://en.wikipedia.org/wiki/Salt_(cryptography)) the passwords too, but given that this is just an example, I'll leave that detail to your implementation.  

In `./models/__init__.py`, (accessible to the entire `models` module) we should write the following:

``` python
from app import db # Grab the db from the top-level app
from marshmallow_sqlalchemy import ModelSchema # Needed for serialization in each model
from werkzeug import check_password_hash, generate_password_hash # Hashing
import hashlib # For session_token generation (session-based auth. flow)

class Base(db.Model):
  """Base PostgreSQL model"""
  __abstract__ = True
  id         = db.Column(db.Integer, primary_key =True)
  created_at = db.Column(db.DateTime, default    =db.func.current_timestamp())
  updated_at = db.Column(db.DateTime, default    =db.func.current_timestamp())

```

The above imports modules and objects necessary for use in your models, as well as defines a `Base` model class that every model should extend to inherit the book-keeping and necessary fields, `id`, `created_at`, and `updated_at`.  

#### User Model

The `User` model in `./models/user.py` will consist of the following:

``` python
from . import *

class User(Base):
  __tablename__ = 'users'

  email           = db.Column(db.String(128), nullable =False, unique =True)
  fname           = db.Column(db.String(128), nullable =False)
  lname           = db.Column(db.String(128), nullable =False)
  password_digest = db.Column(db.String(192), nullable =False)

  def __init__(self, ** kwargs):
    self.email           = kwargs.get('email', None)
    self.fname           = kwargs.get('fname', None)
    self.lname           = kwargs.get('lname', None)
    self.password_digest = generate_password_hash(kwargs.get('password'), None)

  def __repr__(self):
    return str(self.__dict__)


class UserSchema(ModelSchema):
  class Meta:
    model = User

```

The above is pretty self-explanatory.  It outlines several `db` fields, declares a constructor, defines a default string-based representation of the `User` model, and declares a `UserSchema` class that will be used to serialize and deserialize the `User` model to / from `JSON`.  

#### Session Model

The `Session` model in `./models/session.py` will consist of the following:

``` python
from . import *

class Session(Base):
  __tablename__ = 'sessions'

  user_id       = db.Column(db.Integer, db.ForeignKey('users.id'), unique =True, index =True)
  session_token = db.Column(db.String(40))
  update_token  = db.Column(db.String(40))
  expires_at    = db.Column(db.DateTime)

  def __init__(self, ** kwargs):
    user = kwargs.get('user', None)
    if user is None:
      raise Exception() # Shouldn't be the case

    self.user_id       = user.id
    self.session_token = self.urlsafe_base_64()
    self.update_token  = self.urlsafe_base_64()
    self.expires_at    = datetime.datetime.now() + datetime.timedelta(days=7)

  def __repr__(self):
    return str(self.__dict__)

  def urlsafe_base_64(self):
    return hashlib.sha1(os.urandom(64)).hexdigest()


class SessionSchema(ModelSchema):
  class Meta:
    model = Session

```

As we can see, the session model will belong to the user, and be part of a [token-based authentication flow](http://stackoverflow.com/questions/1592534/what-is-token-based-authentication).  Everything in the above code is self-explanatory, and serves as an example session implementation.  


#### Exposing Models to the App

We must import our models into our app in order to have them be exposed to our `manage.py` script responsible for migrating our `db` to match our programmatic schema.  In `./controllers/__int__.py`, I added the following (we'll throw in the imports while we're at it):

``` python
from functools import wraps
from flask import request, jsonify, abort
import os

# Import module models
from app.accounts.models.user import *
from app.accounts.models.session import *

```


For other models and controllers you add with database connection you can safely run the following in the root of your project to migrate your database:

``` bash
# Initialize migrations
python manage.py db init
# Create a migration
python manage.py db migrate
# Apply it to the DB
python manage.py db upgrade
```

Now if you connect to your `Postgres` database, you should see two new tables, `users` and `sessions`!  The migration also creates an index on foreign-key `user_id` in `sessions`, for fast access of sessions by their owning user's `id`.  

That's it for models. 

### Additional Features Added
In addition to the flask application I have added some useful encoding features that can be leveraged by your application. 
Because we leverage numpy arrays all the time when calculating doc-by-vocab matricies I have included some encoding techniques for 2D numpy matricies which I will review soon.
#### Recommendations:
If you are using Heroku or AWS EC2/EB you have a limited number of RAM and in-memory space to store your json data. As such it is recommended that you leverage SVDs on your doc-by-vocab matricies to reduce the dimensionality of your data. Because text-data is ALWAYS dimensionally reducible you should leverage the techniques covered in class in your application. To have fast responses and limited logic I would recommend to pre-process all of your data structures and numpy arrays and store them in some storage system. Two storage systems that I would recommend include: Amazon S3 and Redis. 
##### Amazon S3
After setting up an AWS account and buying some space on your S3 server you can easily put data into your S3 bucket with this simple command:
``` bash
curl --verbose -A "<PASSWORD>" -T <FILE_NAME.EXTENSION> https://s3.amazonaws.com/<YOUR_LOCATION>
```
I would recommend storing all your datastructures in json files and pushing those jsons to S3 in your pre-processing stages, and pulling from S3 at run-time be leveraging the encoding techniques that I have included in `app.irsystem.models.helpers`. 
``` python
class NumpyEncoder(json.JSONEncoder):

    def default(self, obj):
        """If input object is an ndarray it will be converted into a dict 
        holding dtype, shape and the data, base64 encoded.
        """
        if isinstance(obj, np.ndarray):
            if obj.flags['C_CONTIGUOUS']:
                obj_data = obj.data
            else:
                cont_obj = np.ascontiguousarray(obj)
                assert(cont_obj.flags['C_CONTIGUOUS'])
                obj_data = cont_obj.data
            data_b64 = base64.b64encode(obj_data)
            return dict(__ndarray__=data_b64,
                        dtype=str(obj.dtype),
                        shape=obj.shape)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder(self, obj)
        
def json_numpy_obj_hook(dct):
    """Decodes a previously encoded numpy ndarray with proper shape and dtype.
    :param dct: (dict) json encoded ndarray
    :return: (ndarray) if input was an encoded ndarray
    """
    if isinstance(dct, dict) and '__ndarray__' in dct:
        data = base64.b64decode(dct['__ndarray__'])
        return np.frombuffer(data, dct['dtype']).reshape(dct['shape'])
    return dct
```

I will show you how to use these encoding techniques below:
``` python
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.helpers import json_numpy_obj_hook
# Dump numpy array into a json file 
json.dump(NUMPY_ARRAY_NAME, open('NUMPY_ARRAY_NAME.json', 'w'), cls=NumpyEncoder)
# Read numpy array from a json file (where FILE_NAME is an S3 location or local file)
NUMPY_ARRAY_NAME = json.load(FILE_NAME, object_hook=json_numpy_obj_hook, encoding='utf8')
```
##### Redis
Redis is an in-memory data structure store, used as a database, cache and message broker. It supports data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs and geospatial indexes with radius queries. Redis has built-in replication, Lua scripting, LRU eviction, transactions and different levels of on-disk persistence, and provides high availability via Redis Sentinel and automatic partitioning with Redis Cluster. In this application I will be leveraging the python bindings provided by [redis-py](https://github.com/andymccurdy/redis-py) which allow for me to interact with the available redis cluster using python. You can read more about Redis and its useful for ML applications via its in-memory nature [here](https://redis.io/documentation). 
You can install redis by clicking [here](http://download.redis.io/redis-stable.tar.gz) or running `wget http://download.redis.io/redis-stable.tar.gz`
After cd-ing into the directory with the tar file, run the following:
``` bash
tar xvzf redis-stable.tar.gz
cd redis-stable
make
make test
redis-server
```
Check if redis-server is up by running and getting PONG as a result, **hehe :)**
``` bash
$ redis-cli ping
PONG
```
You can modify the Redis DB by running: 
``` bash
$ redis-cli
redis 127.0.0.1:6379> ping
PONG
redis 127.0.0.1:6379> set mykey somevalue
OK
redis 127.0.0.1:6379> get mykey
"somevalue"
```
At this point in time you are able to use the RedisConn class that I defined and the Matrix operation.
To create a Redis connection to the redis cluster you will execute the following:
``` python
rConn = RConn(name='YOUR_SERVER_NAME',host='localhost', port=6379, db=0,max_execs=3,timeout=10,block_size=256)
```    
The normal TCP socket based connection will be available by calling: 
``` python
rDB = rConn.redisDb
```
And if you want to leverage connection pools to manage connections to the redis server with finer grain control an client side sharding you can use this by calling:
``` python
rPool = rConn.rPool
```
For the sake of my Matrix class, I simplified the system by using only the TCP connection (you may modify the classes as you wish).
After having the Redis connection established via `rConn.redisDb` you can simply run the following commands to store a numpy 2D array into Redis (the array must be 2D by design of my encoding):
``` python
# Create RedisConn Class
rConn = RConn(name='YOUR_SERVER_NAME',host='localhost', port=6379, db=0,max_execs=3,timeout=10,block_size=256)
# Grab TCP Connection
rDB = rConn.redisDb
# Store numpy array and return the original numpy array
mat = rConn.store_numpy('my_numpy_array',NUMPY_ARRAY)
rDB.set('my_numpy_array_data',NUMPY_ARRAY.shape)
```
These functions will be used for pre-processing. It is necessary to know the shape of the NUMPY array as it is required for the decoding portion of the Matrix class, so you will store the shape of your input numpy array in Redis as well. As such, at run-time you will run the following to grab the 2D numpy array from Redis:
``` python
if (rDB.exists('my_numpy_array_data')):
		pipe = rDB.pipeline()
		keys = ['my_numpy_array_data']
		[pipe.get(k) for k in keys]
		result = pipe.execute()
		data = {k:result[i] for i,k in enumerate(keys)}
		d_b_v_shape = [int(i)for i in data['my_numpy_array_data'][1:-2].split(',')]
		NUMPY_ARRAY = Matrix('my_numpy_array',d_b_v_shape[0],d_b_v_shape[1],rDB).get_numpy_matrix()
```
You should leverage the pipeline() feature if you are going to be calling more than one (non 2D numpy array) value from Redis. Pipelines are a subclass of the base Redis class that provide support for buffering multiple commands to the server in a single request. They can be used to dramatically increase the performance of groups of commands by reducing the number of back-and-forth TCP packets between the client and server. In the example above there is only 1 in the array, but you can get any number of values you want, in order of requested, given the keys. The specifics of how we build the numpy_matrix are wrapped and hidden from site, but in essence you are creating multiple data blocks that contain portions of the numpy array, and as such the array isnt stored at the key: `my_numpy_array` but instead spread across multiple keys and aggregated at run-time by calling `.get_numpy_matrix()`. You may modify the encoding and decoding if you want to improve the implementation. 
What needs to be noted is that this Redis cluster is only localhost at this point time and will require some DevOps work to get it setup in production. 
I will need to elaborate this README a bit to include how to setup Redis using Amazon ElastiCache for that is a dev ops deployment method for EC2 and EB applications.
You can read more about this type of deployment [here](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.ElastiCache.html). 

## Step-By-Step Guide
### 1. Cloning the repository from Git
```bash
cd ~
git clone https://github.com/CornellNLP/CS4300_Flask_template.git
cd CS4300_Flask_template
```
### 2. Setting up your virtual environment
```bash
# My virtual environment here will be called: venv
virtualenv venv
# Activate the environment
source venv/bin/activate
# Install all dependencies into the virtual environment, this will be done by Heroku and AWS as well
pip install -r requirements.txt
```
If you wish to add any dependencies for future development just do this:
``` bash
pip install <MODULE_NAME>
pip freeze > requirements.txt
```
### 3. Ensuring environment variables are present
``` bash
# Override cd by adding this to your .?rc file (? = bash, zsh, fish, etc), I'll use bash in this example:
echo "source `which activate`" >> ~/.bashrc
# Reload your shell
source ~/.bashrc
# You should have a .env file, if not touch .env 
# After running this you should get the APP_SETTINGS
ECHO $APP_SETTINGS
# Reactivate the environment because you just reloaded the shell
source venv/bin/activate
```
### 4. Setting up Postgres Backend
First install Postgres MacApp or Postgres manually. Then run the following code after Postgres server is up:
``` bash
# Enter postgres command line interface
$ psql
# Create your database which I will call my_app_db in this example, but you can change accordingly
CREATE DATABASE my_app_db;
# Quit out
\q
```
### 5. Check to see if app runs fine by running in localhost:
``` bash
python run.py
```
At this point the app should be running on [http://localhost:5000/](http://localhost:5000/). Navigate to that URL in your browser.
### 6. Push to heroku
I have included the Procile which leverages gunicorn which you can read more about [here](https://devcenter.heroku.com/articles/python-gunicorn) for deployment. 
To setup heroku and push this app to there you will run the following:
First you must install the heroku-cli; the installation instructions can be found [here](https://devcenter.heroku.com/articles/heroku-cli)
After, with your github located at the remote origin you will run the following commands to push to your heroku app.
``` bash
# Login with your heroku credentials
$ heroku login
Enter your Heroku credentials:
Email: <YOUR EMAIL>
Password: <YOUR PASSWORD>
$ heroku create <YOUR_WEBSITE_NAME>
$ git push heroku master
```
Before being able to interact with this application you will go to your Heroku dashboard and find your app.
This will probably be here: `https://dashboard.heroku.com/apps/<YOUR_WEBSITE_NAME>`. 
On that page you will need to modify your environmental variabls (remember your .env??) by navigating to 
`https://dashboard.heroku.com/apps/<YOUR_WEBSITE_NAME>/settings`, clicking `Reveal Config Vars` and in left box below DATABASE_URL write:
`APP_SETTINGS` and in the box to the right write: `config.ProductionConfig`. In essence you are writing `export APP_SETTINGS=config.ProductionConfig` in .env using Heroku's UI.
You lastly will run:
``` bash
heroku ps:scale web=1
```
You may now navigate to `https://<YOUR_WEBSITE_NAME>.herokuapp.com` and see your app in production. From now on, you can continue to push to Heroku and have a easy and well-managed dev flow into production. 
### 7. Setting up App in Amazon Elastic Computing Cloud (EC2) /Elastic Beanstalk (EB) with Redis
**TODO**


