"""
Routes and views for the Flask application.
"""

from datetime import datetime
from flask import render_template, request, session, redirect, url_for
from CourseGrab import app
from CourseGrab.models.sql_client import Client
from CourseGrab import google


@app.route('/')
@app.route('/home')
def index():
    #access_token = session.get('access_token')
    #if access_token is None:
    #    return redirect(url_for('sign_in'))
 
    #access_token = access_token[0]
    #from urllib2 import Request, urlopen, URLError
 
    #headers = {'Authorization': 'OAuth '+access_token}
    #req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
    #              None, headers)
    #try:
    #    res = urlopen(req)
    #except URLError, e:
    #    if e.code == 401:
    #        # Unauthorized - bad token
    #        session.pop('access_token', None)
    #        return redirect(url_for('sign_in'))
    #    return res.read()
 
    #return res.read()
    return render_template('index.html')

@app.route('/sign_in')
def sign_in():
    callback = url_for('authorized', _external = True)
    return google.authorize(callback=callback)
 
 
 
@app.route('/oauth2callback')
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))
 
 
@google.tokengetter
def get_access_token():
    return session.get('access_token')




#@app.route('/submitted', methods=['POST'])
#def submit_request():
#    if request.method == 'POST':
#        course_code = request.form["course_number"]
#        client = Client()
#        client.submit_request("nsun200@live.com", course_code)
#        client.connection.close()
#        return render_template("success.html")


#@app.route('/sign_in')
#def sign_in():
#    return render_template('sign_in.html')





@app.errorhandler(400)
def bad_request(e):
    return "400 error", 400


@app.errorhandler(404)
def page_not_found(e):
    return "404 error", 404


@app.errorhandler(500)
def internal_server_error(e):
    return "500 error", 500