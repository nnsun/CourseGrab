# CourseGrab

Need to add a course but there are no empty slots? Instead of checking for an open slot constantly throughout the day, let CourseGrab do it for you! Simply enter the course ID of the course you want to enroll in, and we'll send you a notification email when the course opens up!

Deployed Spring 2017. Hosted at https://coursegrab.me. 

Built for BigRed//Hacks 2016 by Chase Thomas and Ning Ning Sun

Winner: ***"Best Cornell-Related Hack"*** - awarded by Andreessen Horowitz

Honorable mention: ***"Best Use of Microsoft Technology"*** - awarded by Microsoft

## Getting started

The project itself consists of two parts.

There's the webapp code which is contained in this repo and hosted on a DigitalOcean Ubuntu 16.04 VPS running Apache. It is written in Flask. It has basic Google authentication and allows the user to track up to three courses. 

The time-triggered notifier app is hosted in a [separate repository](https://github.com/nnsun/CourseGrabNotifier) and is written in C#. This is deployed using Azure Functions. Every minute, it will check the statuses of all tracked courses. For all open courses, it will send a notification email to any users who are tracking it and haven't already been notified about the particular opening. That way, a user will not get spammed by emails for the same course in a short period of time. If a particular open course becomes closed but opens up at a later time, users will be notified again. 

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

7. Set up your global variables. CourseGrab uses a SQL database hosted in Azure, as well as a Google client secret and a SendGrid API key for sending notification emails. These are accessed via environment variables in order to avoid storing the credentials publically online. 
ODBC is used to connect to the database, and the variables are as follows: ```DB_SERVER```, the database address; ```DB_NAME```, the name of the database; ```DB_USERNAME```, the username; and ```DB_PASSWORD```, the password.
The Google OAuth 2.0 client secret is defined as ```GOOGLE_CLIENT_SECRET```, and the SendGrid API key is ```SENDGRID_API_KEY```.

8. Start the local server.  
 ```python runserver.py```
 
9. To exit the virtual environment, use ```deactivate```.

### Running the notifier program

Since the notifier program is specially built to work with Azure Functions, the best way to run it locally is with the Azure SDK. [This guide](https://blogs.msdn.microsoft.com/webdev/2016/12/01/visual-studio-tools-for-azure-functions/) helps explain the steps involved. The NuGet packages HtmlAgilityPack and Sendgrid are required (they will be installed automatically by the Azure Functions runtime). 
