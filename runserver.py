"""
This script runs the CourseGrab application using a development server.
"""

from os import environ
from CourseGrab import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        # Order of PORT assignments in try/except switched in order
        # to keep port constant when debugging
        PORT = 5555
    except ValueError:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    app.run(HOST, PORT)
    