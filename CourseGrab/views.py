"""
Routes and views for the Flask application.
"""

from flask import render_template, request, session, redirect, url_for, flash
from urllib2 import Request, urlopen, URLError
import json
import bs4
import requests
from CourseGrab import app as application
from CourseGrab.models.db.sql_client import Client
from CourseGrab import google


@application.route('/')
def index():
    courses = None
    access_token = session.get('access_token')
    course_list = []
    if access_token is not None:
        try:
            user_dict = get_user_dict()
        except Exception:
            callback = url_for('authorized', _external = True)
            return google.authorize(callback=callback)
        user_id = user_dict["id"]
        client = Client()
        course_list = client.get_courses(user_id)
    return render_template('index.html', course_list = course_list)


@application.route('/sign_in')
def sign_in():
    callback = url_for('authorized', _external = True)
    return google.authorize(callback=callback)


@application.route('/oauth2callback')
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    user_dict = get_user_dict()
    user_id = user_dict["id"]
    user_email = user_dict["email"]
    client = Client()
    client.add_user(user_id, user_email)
    return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


@application.route('/submitted', methods = ['POST'])
def submit_request():
    if session.get('access_token') is None:
        flash("Please sign in first.")
    else:
        user_dict = get_user_dict()
        user_id = user_dict["id"]
        course_code = request.form["course_number"]
        client = Client()
        try:
            client.submit_request(user_id, course_code)
            client.connection.close()
        except UserWarning as err:
            flash(str(err))
    return redirect(url_for('index'))


@application.route('/remove/<int:course_num>', methods = ['POST'])
def remove(course_num):
    if session.get('access_token') is None:
        flash("Your session has expired. Please sign in again.")
    else:
        user_dict = get_user_dict()
        user_id = user_dict["id"]
        client = Client()
        client.remove_course(user_id, course_num)
    return redirect(url_for('index'))


@application.route('/sign_out')
def sign_out():
    # remove the token from the session if it's there
    session.pop('access_token', None)
    return redirect(url_for('index'))


@application.route('/api/<int:course_num>', methods = ['GET'])
def course_status_api(course_num):
    return get_course_status(course_num)


def get_user_dict():
    access_token = session.get('access_token')
    if (access_token is None):
        callback = url_for('authorized', _external=True)
        return google.authorize(callback = callback)
    access_token = access_token[0]
    headers = {'Authorization': 'OAuth ' + access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    res = urlopen(req)
    return json.loads(res.read())


@application.errorhandler(400)
def bad_request(e):
    return "400 error", 400


@application.errorhandler(404)
def page_not_found(e):
    return "404 error", 404


@application.errorhandler(500)
def internal_server_error(e):
    return "Looks like you ran into a bug! Turns out making a website is kind of hard. We will fix this someday but in the meantime, just <a href='https://coursegrab.me'>click here</a> to return to the main page. Refreshing the page almost always fixes the problem.", 500

def get_semester():
    roster_page = "https://classes.cornell.edu"
    roster_request = requests.get(roster_page)
    roster_request.raise_for_status()
    split_url = roster_request.url.split('/')
    if split_url[-1] == '':
        return split_url[-2]
    else:
        return split_url[-1]

def get_course_status(course_num):
    client = Client()
    subject = client.get_course_subject(course_num)
    if subject is None:
        return None
    semester = get_semester()
    subject_url = "http://classes.cornell.edu/browse/roster/" + semester + "/subject/" + subject
    subject_page = requests.get(subject_url)
    subject_page.raise_for_status()
    subject_bs4 = bs4.BeautifulSoup(subject_page.text, "html.parser")
    course_code_tags = subject_bs4.find_all("strong", class_="tooltip-iws")
    for tag in course_code_tags:
        course_code = int(tag.getText().strip())
        if course_num == course_code:
            section = tag.parent.parent.parent
            status = section.find_all('li', class_ = "open-status")[0].i["class"][-1]
            if "open-status-open" in status:
                return "open"
            if "open-status-closed" in status:
                return "closed"
            if "open-status-warning" in status:
                return "waitlist"
            if "open-status-archive" in status:
                return "archive"
