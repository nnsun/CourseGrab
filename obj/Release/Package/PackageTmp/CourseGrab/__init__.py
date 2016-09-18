"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__,static_folder='static')

import CourseGrab.views
