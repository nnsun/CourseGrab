"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, send_from_directory, request
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

@app.route('/obey', methods=['POST'])
def edit_csv():
    error = None
    if request.method == 'POST':
        with open("scripts/ledger.csv","a") as fh:
            fh.write(request.form['email']+","+request.form['course_number']+"\n")
        print (__file__)
        return render_template("success.html")



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
