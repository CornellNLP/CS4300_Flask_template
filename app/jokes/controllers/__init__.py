# Import flask deps
from flask import request, render_template, \
	flash, g, session, redirect, url_for, jsonify, abort

# For decorators around routes
from functools import wraps 

# Import the db object from main app module
from app import db 

# Marshmallow 
from marshmallow import ValidationError

# Import socketio for socket creation in this module 
from app import socketio

# Import module models 
from ..models.joke import *

# IMPORT THE BLUEPRINT APP OBJECT 
from app.jokes import jokes 