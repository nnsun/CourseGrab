# CourseGrab
A web app built with Flask, Python, HTML, and CSS.

Every Cornell student runs into trouble with the hectic course signup system, adding some very unneeded stress to the semester.

Need to add a course but there are no empty slots? Give us your email address and the five digit course ID of the lecture or discussion you want to join, and we'll email you when the course is open!

Deploying Spring 2017. Temporary hosted at http://cornellcoursegrab.azurewebsites.net/. 

Built for Big Red Hacks 2016
by Chase Thomas and Ning Ning Sun

Winner: best Cornell-related hack

Honorable mention: Best use of Microsoft Azure

### Getting Started
1. Install [Python 2.7](https://www.python.org/downloads/) if you haven't already.

2. You should now have pip installed. Now install virtualenv so you can create a virtual Python environment  
 ```pip install virtualenv```

3. Clone the project.  
 ```git clone https://github.com/nnsun/CourseGrab.git```  
 ```cd CourseGrab```

4. Create a folder for your virtual environment. On Windows this is  this is ```env\scripts\activate```; on Unix run ```. venv/bin/activate```. 

5. Install the dependencies in requirements.txt.  
 ```pip install -r requirements.txt```

6. Start the local server.  
 ```python runserver.py```

7. To exit the virtual environment, use ```deactivate```. 
