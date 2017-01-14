"""
The flask application package.
"""
from flask import Flask
from flask_oauth import OAuth


app = Flask(__name__,static_folder='static')

import CourseGrab.views
