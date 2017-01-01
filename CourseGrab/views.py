"""
Routes and views for the Flask application.
"""

from datetime import datetime
from flask import render_template, send_from_directory, request
from CourseGrab import app
from CourseGrab.models.sql_client import Client



"""
Display the home page
"""
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


"""

"""
@app.route('/submitted', methods=['POST'])
def submit_request():
    if request.method == 'POST':
        email = request.form["email"]
        course_code = request.form["course_number"]
        client = Client()
        client.submit_request(email, course_code)
        return render_template("success.html")

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/log_in')
def log_in():
    return render_template('log_in.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

#@apply.route('/signup')
#def signup():
#    if request.method == 'GET':
#        name = request.form["email"]
#        email = request.form["email"]
#        phone_number = request.form["phone_number"]
#        send_email = True


    # the code below is executed if the request method
    # was GET or the credentials were invalid

#@app.route('/contact')
#def contact():
#    """Renders the contact page."""
#    return render_template(
#        'contact.html',
#        title='Contact',
#        year=datetime.now().year,
#        message='Your contact page.'
#    )

#@app.route('/about')
#def about():
#    """Renders the about page."""
#    return render_template(
#        'about.html',
#        title='About',
#        year=datetime.now().year,
#        message='Your application description page.'
#    )
