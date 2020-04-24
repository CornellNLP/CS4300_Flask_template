from flask import Blueprint

# Define a Blueprint for this module (mchat)
# note: __name__ is set to __main__ if executed as the main program. But if imported from another module, it is set to module's name (jokes)
jokes = Blueprint('jokes', __name__, url_prefix='/api')

# Import all controllers
from .controllers.jokes_controller import *     