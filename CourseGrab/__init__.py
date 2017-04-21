"""
The Flask application package.
"""
from flask import Flask
from flask_oauth import OAuth
import random
import string
import os

app = Flask(__name__,static_folder='static')

app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
oauth = OAuth()

test = os.getenv("DB_NAME")
if (test is None):
    raise Exception('wtf')
secret = os.getenv("GOOGLE_CLIENT_SECRET")
google = oauth.remote_app('google',
                          base_url = 'https://www.google.com/accounts/',
                          authorize_url = 'https://accounts.google.com/o/oauth2/auth',
                          request_token_url = None,
                          request_token_params = {'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url = 'https://accounts.google.com/o/oauth2/token',
                          access_token_method = 'POST',
                          access_token_params = {'grant_type': 'authorization_code'},
                          consumer_key = "676925479214-9pvc8mn88dp46cl5dothrmbt5efvfjth.apps.googleusercontent.com",
                          consumer_secret = secret)
#			  consumer_secret = 'aBIsexwSEzOmjzRkblcJALf8')


import CourseGrab.views
