"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from CourseGrab import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    if  _email and _password:
        return json.dumps({'html':'<span>All fields good</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

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
