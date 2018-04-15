from flask import Blueprint
from collections import defaultdict

# Define a Blueprint for this module (mchat)
irsystem = Blueprint('irsystem', __name__, url_prefix='/',static_folder='static',template_folder='templates')

# Import all controllers
from controllers.search_controller import *
