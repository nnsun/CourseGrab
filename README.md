# CourseGrab

Every Cornell student runs into trouble with the hectic course signup system, adding some very unneeded stress to the semester.

Need to add a course but there are no empty slots? Give us your email address and the five digit course ID of the lecture or discussion you want to join, and we'll email you when the course is open!

Deploying Spring 2017. Temporary hosted at http://cornellcoursegrab.azurewebsites.net/. 

Built for BigRed//Hacks 2016
by Chase Thomas and Ning Ning Sun

Winner: best Cornell-related hack, awarded by Andreessen Horowitz
Honorable mention: best use of Microsoft Azure, awarded by Microsoft

## Getting started

This project is entirely hosted on Microsoft Azure. It consists of two parts. 
The webapp code, which is written in Flask, is located in the /CourseGrab folder. It has basic Google authentication and allows the user to track up to three courses. 
The time-triggered notifier app is in /CourseGrabNotifier and is written in C#. This is deployed using Azure Functions. Every minute, it will check the statuses of all tracked courses. For all open courses, it will send a notification email to any users who are tracking it and haven't already been notified about the particular opening. That way, a user will not get spammed by emails for the same course in a short period of time. If a particular open course becomes closed but opens up at a later time, users will be notified again. 

### Running the webapp on localhost

1. Install [Python 2.7](https://www.python.org/downloads/) if you haven't already.

2. You should now have pip installed. Now install virtualenv so you can create a virtual Python environment  
 ```pip install virtualenv```

3. Clone the project.  
 ```git clone https://github.com/nnsun/CourseGrab.git```  
 ```cd CourseGrab```

4. Create a folder for your virtual environment inside the webapp folder. 
```cd CourseGrab```
```virtualenv env```

5. Enter the virtual environment. Use ```env\Scripts\activate``` on Windows; on Unix, use ```. env/bin/activate```.

6. Install the dependencies in requirements.txt.  
 ```pip install -r requirements.txt```

7. Set up your environment variables. CourseGrab uses a SQL database hosted in Azure, as well as a Google client secret. These are accessed via environment variables in order to avoid storing the credentials publically online. ODBC is used to connect to the database in /CourseGrab/CourseGrab/models/sql_client.py, and the variables are as follows: ```DB_SERVER```, the database address; ```DB_NAME```, the name of the database; ```DB_USERNAME```, the username; and ```DB_PASSWORD```, the password.

The Google OAuth 2.0 client secret is used in /CourseGrab/CourseGrab/__init__.py, and is defined as ```GOOGLE_CLIENT_SECRET```.

8. Start the local server.  
 ```python runserver.py```
 
9. To exit the virtual environment, use ```deactivate```.
