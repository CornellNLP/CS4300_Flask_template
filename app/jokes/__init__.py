from flask import Blueprint

# Define a Blueprint for this module (mchat)
jokes = Blueprint('jokes', __name__, url_prefix='/jokes')

# Import all controllers
from .controllers.jokes_controller import *