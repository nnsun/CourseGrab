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
        client.connection.close()
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


@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')


@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')


@app.errorhandler(400)
def bad_request(e):
    return "400 error", 400


@app.errorhandler(404)
def page_not_found(e):
    return "404 error", 404


@app.errorhandler(500)
def internal_server_error(e):
    return "500 error", 500