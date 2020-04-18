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
from app.accounts import accounts as accounts
app.register_blueprint(accounts)
print("importing full irsystem")
from app.irsystem import irsystem as irsystem
app.register_blueprint(irsystem)

# Initialize app w/SocketIO
socketio.init_app(app)

from app.irsystem.models.search import open_datastructures
@app.before_first_request
def before_first_request():
	open_datastructures()

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
  return render_template("404.html"), 404
