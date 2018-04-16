# Import flask deps
from flask import request, render_template, \
	flash, g, session, redirect, url_for, jsonify, abort

# For decorators around routes
from functools import wraps

# Import for pass / encryption
from werkzeug import check_password_hash, generate_password_hash

# Import the db object from main app module
from app import db

# Marshmallow
from marshmallow import ValidationError

# Import module models
from app.irsystem.models.comment import Comment

# IMPORT THE BLUEPRINT APP OBJECT
from app.irsystem import irsystem
