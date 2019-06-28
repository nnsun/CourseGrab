# CourseGrab

*This project is [now being maintained by Cornell App Dev](https://github.com/cuappdev/course-grab) and hosted at [coursegrab.cornellappdev.com](coursegrab.cornellappdev.com) as of May 2019.*

Need to add a course but there are no empty slots? Instead of constantly checking for an open slot throughout the day, adding undue stress to your busy life, let CourseGrab do it for you! Simply enter the course ID of the course you want to enroll in, and we'll send you a notification email when the course opens up!

Deployed Spring 2017

Built for BigRed//Hacks 2016 by Chase Thomas and Ning Ning Sun

Winner: ***"Best Cornell-Related Hack"*** - awarded by Andreessen Horowitz

Honorable mention: ***"Best Use of Microsoft Technology"*** - awarded by Microsoft

## Project Details

The project itself consists of two parts.

There's the webapp code which is contained in this repo and hosted on a DigitalOcean Ubuntu 16.04 VPS running Apache. It is written in Flask. It has basic Google authentication and allows the user to track up to three courses. 

The time-triggered notifier app is hosted in a [separate repository](https://github.com/nnsun/CourseGrabNotifier) and is written in C#. This is deployed using Azure Functions. Every minute, it will check the statuses of all tracked courses. For all open courses, it will send a notification email to any users who are tracking it and haven't already been notified about the particular opening. That way, a user will not get spammed by emails for the same course in a short period of time. If a particular open course becomes closed but opens up at a later time, users will be notified again. 

### Running the webapp on localhost

1. Install [Python 2.7](https://www.python.org/downloads/) if you haven't already.

2. You should now have pip installed. Now install virtualenv so you can create a virtual Python environment.  
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
You may need to also install an ODBC driver in order to access your SQL database. 
 
7. Create a new project in the [Google App Engine](https://cloud.google.com/appengine/). In the API Manager, make a set of new OAuth2 client ID credentials. You will be given a client ID and a client secret. Next, add ```http://127.0.0.1:5000``` to the list of authorized JavaScript origins and ```http://127.0.0.1:5000/oauth2callback``` to the list of authorized redirect URIs. 

8. Set up your global variables. CourseGrab uses a SQL Server database hosted in Azure, as well as a Google client secret and a SendGrid API key for sending notification emails. These are accessed via environment variables in order to avoid storing the credentials publically online. 
ODBC is used to connect to the database, and the variables are as follows: ```DB_SERVER```, the database address; ```DB_NAME```, the name of the database; ```DB_USERNAME```, the username; and ```DB_PASSWORD```, the password. These values are declared in the CourseGrab/CourseGrab/models/db/config.py file, which is imported by CourseGrab/CourseGrab/models/sql_client.py. The Google OAuth 2.0 client secret, ```GOOGLE_CLIENT_SECRET```, is located in CourseGrab/CourseGrab/config.py, and is imported by CourseGrab/CourseGrab/\_\_init\_\_.py. Also, change the consumer_key value in CourseGrab/CourseGrab/\_\_init\_\_.py to your Google App Engine client ID.
The SendGrid API key is ```SENDGRID_API_KEY```. This is only used in the Azure Functions script.

9. Start the local server.  
```python runserver.py```  
You should now be able to access a full-featured localhost version of the website at ```127.0.0.1:5000```
 
 10. To exit the virtual environment, use ```deactivate```.

### Running the notifier program

Since the notifier program is specially built to work with Azure Functions, the best way to run it locally is with the Azure SDK. [This guide](https://blogs.msdn.microsoft.com/webdev/2016/12/01/visual-studio-tools-for-azure-functions/) helps explain the steps involved. The NuGet packages HtmlAgilityPack and Sendgrid are required (they will be installed automatically by the Azure Functions runtime). 
