"""
Routes and views for the Flask application.
"""

from datetime import datetime
from flask import render_template, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
import pyodbc
import os
from CourseGrab import app






#server = "tcp:coursegrabdb.database.windows.net"
#database = "coursegrabdb"
#username = "nnsun"
#password = os.getenv("EMAIL_PASSWORD")
#connection = pyodbc.connect("DRIVER={ODBC Driver 13 for SQL Server};SERVER="
#                            + server + ";DATABASE=" + database + ";UID=" 
#                            + username + ";PWD=" + password)
#cursor = connection.cursor()


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template('index.html')


@app.route('/obey', methods=['POST'])
def edit_csv():
    if request.method == 'POST':
        with open("WebJob/ledger.csv","a") as fh:
            fh.write(request.form['email']+","+request.form['course_number']+"\n")
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
