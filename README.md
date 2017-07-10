# CourseGrab

Need to add a course but there are no empty slots? Instead of constantly checking for an open slot throughout the day, adding undue stress to your busy life, let CourseGrab do it for you! Simply enter the course ID of the course you want to enroll in, and we'll send you a notification email when the course opens up!

Deployed Spring 2017. Hosted at https://coursegrab.me. 

Built for BigRed//Hacks 2016 by Chase Thomas and Ning Ning Sun

Winner: ***"Best Cornell-Related Hack"*** - awarded by Andreessen Horowitz

Honorable mention: ***"Best Use of Microsoft Technology"*** - awarded by Microsoft

## Project Details

The project itself consists of two parts.

There's the webapp code which is contained in this repo and hosted on a DigitalOcean Ubuntu 16.04 VPS running Apache. It is written in Flask. It has basic Google authentication and allows the user to track up to three courses. 

The time-triggered notifier app is hosted in a [separate repository](https://github.com/nnsun/CourseGrabNotifier) and is written in C#. This is deployed using Azure Functions. Every minute, it will check the statuses of all tracked courses. For all open courses, it will send a notification email to any users who are tracking it and haven't already been notified about the particular opening. That way, a user will not get spammed by emails for the same course in a short period of time. If a particular open course becomes closed but opens up at a later time, users will be notified again. 
