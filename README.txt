'
'
'
'
'
'
Welcome to my 15-112 Final Project Program!
'
'
'
'
'
'

PROJECT DESCRIPTION: CMU Course Scheduler

The scope of this project is to make it easier for Carnegie Mellon University Students
to choose courses for upcoming semesters. The program obtains the courses offered in
an upcoming semester from the HTML page. This is the link to the raw HTML data for
the courses:

https://enr-apps.as.cmu.edu/assets/SOC/sched_layout_spring.htm

My program accesses this webpage and processes the data to get all of the course
information for the ones offered in Doha, Qatar. It then gives the user the
ability to pick the courses they want to take next semester. The user picks
the maximum number of units and is also able to add personal times to the
schedule. The program then determines which courses would fit with each other the
best and calculates this course plan. The user is able to view this course plan
and save it to a remote server for later retrieval.

This makes for a simple to use and comfortable course scheduler.








INSTALLATION:

Required Python Packages: requests, socket, Tkinter, and BeautifulSoup


requests library - https://pypi.python.org/pypi/requests/2.6.0

socket library - part of built-in python library

Tkinter - part of built-in python library

BeautifulSoup installation instrucitons - http://www.pythonforbeginners.com/beautifulsoup/beautifulsoup-4-python









USES OF EACH LIBRARY:

requests library - this obtains the HTML text of a webpage using a url

socket library - this creates a connection to the remote server and saves the
	the course plans. It is also used to later retrieve saved course plans.

Tkinter library - this hosts the GUI of the program and gives the user the
	option to interact with the program using buttons, listboxes, etc.

BeautifulSoup - this takes in HTML data and makes it easier to filter through
	HTML text using the attributes and HTML tags



NOTES:

The file prereq.csv is used for obtaining the the prerequisites of CMU courses.
Since CMU, doesn't have an official data file from where to collect all courses
and their prerequisites, I populated the file myself with 10 sample courses and
their respective prerequisites. This is to shhow that my program is able to handle
courses and their prerequisites.


I hope you enjoy the program!
