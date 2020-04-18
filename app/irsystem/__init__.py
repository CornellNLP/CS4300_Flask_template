from flask import Blueprint

# Define a Blueprint for this module (mchat)
irsystem = Blueprint('irsystem', __name__, url_prefix='/',static_folder='static',template_folder='templates')

# Import all controllers
print("importing controllers")
from .controllers.search_controller import *
from app.irsystem.models.search import open_datastructures
open_datastructures()
