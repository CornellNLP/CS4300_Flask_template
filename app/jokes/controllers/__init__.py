from functools import wraps
from flask import request, jsonify, abort
import os

# Import module models
from ..models.joke import *