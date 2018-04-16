import praw
# Gevent needed for sockets
from gevent import monkey
monkey.patch_all()

# Imports
import os
from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy

# Configure app
app = Flask(__name__, static_folder='frontend/dist', template_folder='frontend/')
app.config.from_object(os.environ["APP_SETTINGS"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# DB
db = SQLAlchemy(app)

#reddit obj
reddit = praw.Reddit(user_agent='comment_query', client_id='WsGOFsPaaGtYVQ', client_secret="qPogCXpTh1wZylbQqES6JY04PVw")

# Import + Register Blueprints
from app.irsystem import irsystem as irsystem
app.register_blueprint(irsystem)

# React Catch All Paths
@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/static/<path:path>', methods=['GET'])
def serve_static(path):
    return send_from_directory('frontend/build/static', path)
