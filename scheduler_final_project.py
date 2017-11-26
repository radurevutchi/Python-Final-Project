#
#    15-112: Principles of Programming and Computer Science
#    Python Final Project
#	 See the README file for all details
#    Name      : Radu-Stefan Revutchi
#    AndrewID  : rrevutch

#    File Created: 11/11 14:00
#    Modification History:
#    Start             End
#    11/11 14:00       11/11 18:00
#	 12/11 20:00       12/11 22:30
#	 15/11 17:30       15/11 19:30
#    17/11 14:30       17/11 23:30
#	 18/11 20:00       18/11 22:30
#	 19/11 17:00       19/11 20:30
#    22/11 16:00       22/11 18:00
#	 23/11 18:00       23/11 22:30
#	 25/11 17:00       25/11 23:30






import requests, socket
from bs4 import BeautifulSoup
from Tkinter import *











'''
Courses that won't be included in the course selection:

- Ones that don't have a definite number of units assigned to them
- Ones that don't have a time assigned to them yet

'''





#creates a time class to deal with the different schedules
class WeekSchedule:

	def __init__(self, time):

		#defines a dictionary for each day of the week
		self.time = time
		self.days = {}
		self.days['U'] = []
		self.days['M'] = []
		self.days['T'] = []
		self.days['W'] = []
		self.days['R'] = []


		#takes each time string and divides it up into the individual time pieces
		self.raw_times = self.time.split()

		#calls funciton to fill the dicitonary
		self.fillDays()


	#gets the beginning time of an activity.course during a specific day given
	def getmin(self, day):

		#if there is something during the day, it finds the min
		if self.days[day] != []:
			return min(self.days[day])
		else:
			return None


	#gets the ending time of an activity.course during a specific day given
	def getmax(self, day):

		#if there is something during the day, it finds the max
		if self.days[day] != []:
			return max(self.days[day])
		else:
			return None


	#gets the time pieces in the form of a self.raw_times list and goes through it
	def fillDays(self):


		#Goes through each of the class hours of the course and adds to the dictionary self.days
		for lectures in self.raw_times:
			hours = lectures[-14:]
			weekdays = lectures[:-14]

			#turns the time piece into military time
			range_hours = self.toMilitaryTime(hours)


			#For each day of the week where there are classes, the range of military time will be added
			for a in range(len(weekdays)):
				self.days[weekdays[a]] += range(range_hours[0], range_hours[1] + 1)



	#converts the string in form ##:##@M##:##@M to military time and returns the beginning and end mlitary time
	def toMilitaryTime(self, normaltime):

		##Obtains the beginning times
		beg = normaltime[:7]
		end = normaltime[7:]

		#finds the hour time and multiplies it by 100 to caluclate hours in military time
		begrange = int(beg[:2]) * 100

		begrange += int(beg[3:5])

		if beg[5:7] == 'PM' and int(beg[:2]) !=12:
			begrange += 1200

		#finds the hour time and multiplies it by 100 to caluclate hours in military time
		endrange = int(end[:2]) * 100

		endrange += int(end[3:5])


		#deals with the PM parameter and adds 12 to the hours if necessary
		if end[5:7] == 'PM' and int(end[:2]) !=12:
			endrange += 1200


		return [begrange, endrange]



	#it creates the to string method for printing out
	def __str__(self):

		print self.days







#defines a course class with the course number, name, number of units, time, and professor name if there is one
class Course:

	def __init__(self, number, name, units, time, professor):

		#initializes everything necessary to describe a course including a WeekSchedule object
		self.number = number
		self.name = name
		self.units = units
		self.time = WeekSchedule(time)#time
		self.professor = professor



	#it is a funciton that deals with another Course object
	#It compares itself with another course object to see if they interfere in time
	#returns false if they do not interfere
	def interferes(self, othercourse):


		conflicts = False
		currenttime = []
		othertime = []


		#it goes through each day of the week to check interferernce
		for x in ['U','M','T','W','R']:

			#it uses set union to check for interference
			currenttime = set(self.time.days[x])
			othertime = set(othercourse.time.days[x])

			#if two times overlap by more than 5 minutes, they interfere
			if len(list(currenttime & othertime)) > 5:
				return True


		#returns false if they do not interfere
		return False






#creates the welcome screen for the user to pick between a
class WelcomeScreen():

	def __init__(self):

		self.courses = {}
		#sets up the window layout
		self.master = Tk()
		self.master.title('CMU Course Scheduler')
		self.master.geometry('400x100')


		#sets the button to try login information, calls the function within this class
		self.retrieveButton = Button(self.master,text='Create New Schedule', command = self.create_main_window).grid(row=0, column=0)
		self.newButton = Button(self.master,text='Retrieve Saved Schedule', command = self.get_saved_schedule).grid(row=0, column=1)
		self.newButton = Label(self.master,text='Enter Username').grid(row=1, column=1)
		self.savedusername = Entry(self.master)
		self.savedusername.grid(row=2,column=1)
		self.errorlabel = Label(self.master, text='')
		self.errorlabel.grid(row=3, column=1)



		self.master.mainloop()




	#creates the next step and window of creating a new course plan
	def create_main_window(self):
		self.master.destroy() #kills the current window.
		#creates the prerequisites window
		prereqpage = Prerequisites()




	#uses the username to determine if there is a saved schedule on that name
	def get_saved_schedule(self):

		#gets list of courses from cmu website
		self.courses = self.getcourses()

		#creates socket connection to razak's server
		a = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		a.connect(("86.36.35.17", 15112))

		#logs in to the shat client server
		login(a, 'monkey2', 'banana2')

		#reads the file with the saved plans
		getMail(a)

		#reads the inside lines of the file
		plans = open("savedplans.txt",'r')
		planlist = plans.readlines()
		plans.close()





		plandict = {}

		#turns the file data into a dictionary of every saved course plan entry
		for x in planlist:

			#it splits up the entry into the individual courses
			courselist = x.split()
			if len(courselist) >1:
				plandict[courselist[0]] = courselist[1:]




		#gets the username
		username = self.savedusername.get()


		#checks if the username has a saved entry
		if username in plandict:

			returnplans = open("savedplans.txt","w")

			#Adds every dictionary entry back into the file and send it back
			for person in plandict:
				append1 = ''
				append1 += person
				for course in plandict[person]:
					append1 += ' ' + course
				returnplans.write(append1 + '\n') #appends to the file to return to the server

			returnplans.close()

			#Sends the file back to the razak server
			sendFile(a, 'monkey2', 'savedplans.txt')


			#creates a new display window for the entry
			self.master.destroy() #kills the current window
			displayplan = DisplayResult(self.courses, plandict[username], 0, True) #creates a displayresult object ot display the previously saved course



		#does this if username is not a saved entry
		else:


			#creates a file for returning to the server since it automatically gets deleted when viewed
			returnplans = open("savedplans.txt","w")


			#adds each entry of the dictionary back to the file savedplans.txt
			for person in plandict:
				append1 = ''
				append1 += person
				for course in plandict[person]:
					append1 += ' ' + course
				returnplans.write(append1 + '\n') #appends to the file to return to the server

			returnplans.close()

			#sends the file back to the RAZAK server
			sendFile(a, 'monkey2', 'savedplans.txt')

			#tells the user that tht given username doesn't exist
			self.errorlabel.configure(text='No such username!')


		a.close() #closes the socket connection





	#gets the courses for the Spring semester from cmu's official website
	def getcourses(self):


		#file18 = open('spring18updated.html', 'r')
		#data18 = file18.read()


		result = requests.get("https://enr-apps.as.cmu.edu/assets/SOC/sched_layout_spring.htm")
		soup18 = BeautifulSoup(result.text, 'lxml')
		print len(result.text)
		#soup18 = BeautifulSoup(result.text)
		#soup18 = BeautifulSoup(data18, 'lxml')


		lecturetime = ''
		springcourses = {}



		#goes through each line of the html page
		for course in soup18.find_all('tr'):

			#splits up the line into the course info such as professorr, hours, location, time, number, and course name
			courseinfo = course.find_all('td')


			#checks to make sure this is a course description
			if len(courseinfo) > 8:

				#checks if the line includes the title and number of the course
				if courseinfo[0].text.encode('utf-8').isdigit():

					#resets lecture variables since there might not be any lectures for a specific course
					lecture = False
					lecturetime = ''
					qatar = False

					#gets the course number and course name as strings
					coursenumber = courseinfo[0].text.encode('utf-8')
					coursename = courseinfo[1].text.encode('utf-8')

					#tries to calculate the number of units and gives unit values of -1 if it fails
					try:
						units = int(float(courseinfo[2].text.encode('utf-8')))
					except:
						units = -1



				#checks if the course/lecture is taking place in qatar

				if courseinfo[8].text.encode('utf-8') == 'Doha, Qatar':

					#boolean to state that course takes place in qatar
					qatar = True

					#tries to get a professor name from the professor tab
					try:
						professor = courseinfo[9].text.encode('utf-8')
					except:
						professor = ''


					#checks if there is a lecture involved and records the time
					if courseinfo[3].text.encode('utf-8')[:3] == 'Lec':
						lecture = True
						lecturetime = courseinfo[4].text.encode('utf-8')+courseinfo[5].text.encode('utf-8')+ courseinfo[6].text.encode('utf-8')


					#prints out the course if it is not a lecture but actual class time
					else:

						coursetime = courseinfo[4].text.encode('utf-8')+courseinfo[5].text.encode('utf-8')+ courseinfo[6].text.encode('utf-8')
						coursetime += ' ' + lecturetime

						#creates this exception because 15110 has a technical error on cmu's course search website
						if coursenumber == '15110':
							coursetime = 'UT' + courseinfo[4].text.encode('utf-8')+courseinfo[5].text.encode('utf-8')+ courseinfo[6].text.encode('utf-8')


						#criteria for adding a course to the dictionary of Courses
						#there must be a professor for it, it must have a definite number of units, and there must be a coursetime
						if len(professor) > 2 and units > 0 and len(coursetime) > 4 and qatar:


							#adds the course to the dictionary springcourses
							if coursenumber in springcourses:
								springcourses[coursenumber].append(Course(coursenumber, coursename, units, coursetime, professor))
							else:
								springcourses[coursenumber] = [Course(coursenumber, coursename, units, coursetime, professor)]



		#returns the dictionary of courses for the spring semester
		return springcourses





#Creates a new class for a prerequisite window
#opens the window for the prerequisites
class Prerequisites():

	def __init__(self):

		#opens the file of prerequisites
		prereq = open('prereq.csv', 'r')


		#initilaizes arrays to represent the courses selcted and prerequisites required
		self.taken = {}
		self.selected = []
		self.rawlist = prereq.readlines() #reads the csv file of prerequisites

		#splits up the courese and makes them into readable strings
		for courseinfo in self.rawlist:
			orderedcourses = courseinfo.split(',')
			self.taken[orderedcourses[0]] = orderedcourses[1:-1] + [orderedcourses[-1][:-1]]




		#sets up the window layout and window size
		self.master = Tk()
		self.master.title('Pick Prerequisites')
		self.master.geometry('800x400')


		#sets up the window layout
		Label(self.master, text='Please select which of the following courses you have already taken:').grid(row=0, column=0)


		#SETS UP THE LISTBOXES AND LABELS AND BUTTONS SO THAT THE USER CAN INTERACT
		self.viewcourses = Listbox(self.master, exportselection=0, height=10, width=20)
		self.viewcourses.grid(row=1, column=0)

		self.takencourses = Listbox(self.master, exportselection=0, height=10, width=20)
		self.takencourses.grid(row=1, column=1)

		self.addcourse = Button(self.master, text='Select Course', command=self.add_course, width=20)
		self.addcourse.grid(row=2, column=0)

		self.done = Button(self.master, text='Done', command=self.done)
		self.done.grid(row=2,column=1)

		self.populatecourses()

		self.master.mainloop()





	#adds the courses to the list of prerequisites
	#which the usser has taken previously in her or his wonderful life
	def populatecourses(self):


		#deletes the previous course list of rperequisites
		self.viewcourses.delete(0, END)

		#goes thourhg each of the prerequisites listed and adds it to the listbox
		courses = []
		for x in self.taken.values():
			courses += x

		#sorts the courses and removes duplicates
		courses = list(set(courses))
		courses = sorted(courses)


		#goes through each course and adds it to the list in order
		for a in courses:
			if a not in self.selected:
				self.viewcourses.insert(END, a)



	#adds a course to the listbox and array of courses previously taken
	def add_course(self):
		selection = self.viewcourses.curselection()
		if selection != (): #if a course is selected
			self.selected.append(self.viewcourses.get(selection[0])[:5])
			self.takencourses.insert(END, self.viewcourses.get(selection[0])) #adds course to the listbox of courses previously taken

			self.populatecourses() #refreshes the courses in the prerequisite list


	#destroys the current window and opens up the choosing of a new course plan
	def done(self):
		self.master.destroy()

		newschedule = CreateSchedule(self.selected,{}) #creaetes a new instance of create schedule which allows teh user to select all of the courses he or she has taken





#class the defines the coures which the user may select to take
#Creates the main and most important window: the choosing of courses
class CreateSchedule():

	def __init__(self, selected, taken):

		#sets up the window layout

		self.maxunits = 0
		self.selectedunits = 0
		self.courses = self.getcourses()

		#removes the prerequisitets taken from the courselist
		self.remove_no_prereqs(selected,taken)



		#SETS UP THE LAYOUT OF THE TKINTER WINDOW
		self.master = Tk()
		self.master.title('CMU Course Scheduler')
		self.master.geometry('1000x650')



		#SETS UP LISTBOXES AND BUTTONS AND LABELS
		Label(self.master,height=2, text='These are the courses you can take according to the prerequisitses you have:').grid(row=0, column=0)
		self.coursemenu = Listbox(self.master, exportselection=0, height=20, width=50)
		self.coursemenu.grid(row=1, column=0)

		self.addcourse = Button(self.master, text='Pick Course', command=self.add_course)
		self.addcourse.grid(row=2, column=0)

		#MORE LISTBOXES, LABELS, AND BUTTONS, AND TEXTBOXES
		Label(self.master, text='Add a personal activity?').grid(row=3, column=0, sticky="W")
		Label(self.master, text='Activity Name:').grid(row=4, column=0, sticky="W")
		self.activityname = Entry(self.master)
		self.activityname.grid(row=4, column=0)

		Label(self.master, text='From (hh:mm):').grid(row=5, column=0, sticky="W")
		self.starttime = Entry(self.master)
		self.starttime.grid(row=5, column=0)


		Label(self.master, text='To (hh:mm):').grid(row=6, column=0, sticky="W")
		self.endtime = Entry(self.master)
		self.endtime.grid(row=6, column=0)

		self.addactivity = Button(self.master, text='Add Personal Activity', command=self.add_personal_activity)
		self.addactivity.grid(row=7, column=0)

		self.personalerror = Label(self.master, text='')
		self.personalerror.grid(row=8,column=0)


		#SETS UP THE CHECKLISTS FOR THE DAYS OF THE WORK WEEK IN QATAR: SUNDAY TO THURSDAY
		self.var1 = IntVar()
		self.var2 = IntVar()
		self.var3 = IntVar()
		self.var4 = IntVar()
		self.var5 = IntVar()
		self.sunday = Checkbutton(self.master, text='Sunday', variable = self.var1)
		self.monday = Checkbutton(self.master, text='Monday', variable = self.var2)
		self.tuesday = Checkbutton(self.master, text='Tuesday', variable = self.var3)
		self.wednesday = Checkbutton(self.master, text='Wednesday', variable = self.var4)
		self.thursday = Checkbutton(self.master, text='Thursday', variable = self.var5)
		self.sunday.grid(row=9, column=0, sticky="W")
		self.monday.grid(row=10, column=0, sticky="W")
		self.tuesday.grid(row=11, column=0, sticky="W")
		self.wednesday.grid(row=12, column=0, sticky="W")
		self.thursday.grid(row=13, column=0, sticky="W")







		#SETS UP MORE LISTBOXES AND LABELS AND BUTTONS
		Label(self.master, text='Select your weekly schedule/courses in order of preference: ').grid(row=0, column=1)
		self.selectedmenu = Listbox(self.master, exportselection=0, height=20, width=50)
		self.selectedmenu.grid(row=1, column=1)

		self.resetcourses = Button(self.master, text='Reset', command=self.reset_selection)
		self.resetcourses.grid(row=2, column=1)


		self.unitslabel = Label(self.master, text='Units Selected: 0')
		self.unitslabel.grid(row=3, column = 1)

		self.selectunitslabel = Label(self.master, text='Enter maximum number of units: (min:36)').grid(row=4,column=1)
		self.selectunits = Entry(self.master)
		self.selectunits.grid(row=5,column=1)
		self.submitunits = Button(self.master, text="Confirm Units", command = self.confirm_units)
		self.submitunits.grid(row=6, column=1)
		self.maxunitslabel = Label(self.master, text = '')
		self.maxunitslabel.grid(row=7,column=1)


		self.resetcourses = Button(self.master, text='Calculate Course Plan!', command=self.get_course_plan)
		self.resetcourses.grid(row=8, column=1)

		self.calculateerror = Label(self.master, text='')
		self.calculateerror.grid(row=9, column = 1)


		#INITIALIZES variables relating to personal activites, selected courses, and the list of sorted courses
		self.sortedcourses = []
		self.personaltimes = ''
		self.selectedcourses = []

		self.sort_courses()
		self.update_courses()




		self.master.mainloop()




	#dows this when the max units button is pressed
	#makes sure the number of units is an integer and above 36

	def confirm_units(self):
		maxunits = self.selectunits.get()
		if maxunits.isdigit() and int(maxunits) > 35:
			self.maxunits = int(maxunits)
			self.maxunitslabel.configure(text='Your maximum units are: ' + str(self.maxunits))
		else:
			self.maxunitslabel.configure(text="Wrong answer, please try again!") ##gives error message




	#tries to login and kills the screen if wrong login
	#closes login screen and opens new main screen if login is correct
	def remove_no_prereqs(self, selected, taken):

		removecourses = []
		for x in taken:
			complete_pre = True
			for y in taken[x]:
				if y not in selected:
					complete_pre = False
			if complete_pre == False:
				removecourses.append(x) #appends to the list of courses to remove from the overall list of courses offered in the spring


		#goes thorugh each of the courses in the dicitonary of courses offered
		#and removes it if the prerequisites are not met
		for course in removecourses:
			if course in self.courses:
				del self.courses[course]






	#sorts the courses from the dictionary self.courses and adds it to the sorted list of courses
	def sort_courses(self):

		self.sortedcourses = map(lambda x: int(x), self.courses.keys())
		self.sortedcourses = sorted(self.sortedcourses)
		self.sortedcourses = map(lambda x: str(x), self.sortedcourses)


		#turns the integer courses into strings
		for a in range(len(self.sortedcourses)):
			if len(self.sortedcourses[a]) == 4:
				self.sortedcourses[a] = '0' + self.sortedcourses[a]





	#refreshes the courses after a course has been selected
	def update_courses(self):


		#updates list of courses to select from
		self.coursemenu.delete(0, END) #clears the listbox of courses offered
		for thing in self.sortedcourses:
			if thing not in map(lambda x: x[:5], self.selectedcourses):
				self.coursemenu.insert(END, thing + '  ' + self.courses[thing][0].name) #adds the courses back to the listbox





	#tries to login and kills the screen if wrong login
	#closes login screen and opens new main screen if login is correct
	def add_course(self):

		selection = self.coursemenu.curselection()
		if selection != (): #if a course is selected
			self.selectedcourses.append(self.coursemenu.get(selection[0])[:5])
			self.selectedmenu.insert(END, self.coursemenu.get(selection[0]))

			coursenumber = self.coursemenu.get(selection[0])[:5]
			units = self.courses[coursenumber][0].units
			self.selectedunits += units

			self.unitslabel.configure(text='Units Selected: ' + str(self.selectedunits)) #adds the number to the number of units selected
			self.calculateerror.configure(text='')


		self.update_courses() #refreshes the courses in the listbox





	#tries to login and kills the screen if wrong login
	#closes login screen and opens new main screen if login is correct
	def reset_selection(self):

		self.unitslabel.configure(text='Units Selected: 0')
		self.selectedmenu.delete(0, END)
		self.selectedcourses = []
		self.selectedunits = 0

		self.update_courses()



	#goes thorugh each of the selected courses and starts off with each one one by one
	#Calculates if a course will fit in the plan in order of picked preference
	def get_course_plan(self):

		courseplan = []

		totalunits = 0

		if len(self.selectedcourses) > 0 and self.maxunits != 0: #makes sure the user has selected some units

			courseplan.append(self.selectedcourses[0])
			totalunits += self.courses[self.selectedcourses[0]][0].units
			self.selectedcourses = self.selectedcourses[1:] #adds the first choice plan to the courseplan




			for x in self.selectedcourses: #goes through the remaining courses in selected courses
				conflict = False


				#ges thorugh each one of the courses in the current courseplan
				for y in courseplan:

					if self.courses[x][0].interferes(self.courses[y][0]): #determines if they interfere according to the weekschedule class
						conflict = True

				if not conflict and totalunits + self.courses[x][0].units <= self.maxunits: #if they do not interfere, adds it to the courseplan and updates the number of units
					courseplan.append(x)
					totalunits += self.courses[x][0].units


			self.master.destroy() #destroys the current window

			displayplan = DisplayResult(self.courses, courseplan, totalunits, False) #created displayresult instance to show the courseplan

		else:
			self.calculateerror.configure(text='You did not select any courses yet or select minimum units!') #shows error message






	#adds a personal activity
	def add_personal_activity(self):

		#gets the entries from the user
		start = self.starttime.get()
		end = self.endtime.get()
		activitytype = self.activityname.get()

		#cretaes a dictionary including all of the days of the week
		days = {}
		days['U'] = self.var1.get()
		days['M'] = self.var2.get()
		days['T'] = self.var3.get()
		days['W'] = self.var4.get()
		days['R'] = self.var5.get()


		#makes sure the format of the user entries is correct
		if len(start) == 5 and len(end) == 5 and start[0:2].isdigit() and start[3:5].isdigit() and end[0:2].isdigit() and end[3:5].isdigit() and start[2] == ':' and end[2] == ":" and activitytype:

			startHR = int(start[:2])
			startMIN = int(start[3:5])
			endHR = int(end[:2])
			endMIN = int(end[3:5])

			#makes sure a correct time is entered for beginning and ending times
			if startHR < 24 and endHR < 24 and startMIN < 60 and endMIN < 60 and reduce(lambda x,y: x+y, days.values()) != 0:



				#CONVERTS EVERY TIME TO A TIM EREADABLE BY WEEKSCHEDULE CLASS
				time = ''

				for day in days:
					if days[day] == 1:
						time += day

				if startHR >= 13:
					startHR -= 12
					a = 'PM'

				elif startHR == 12:
					a = 'PM'
				else:
					a = 'AM'

				if endHR >= 13:
					endHR -= 12
					b = 'PM'
				elif endHR == 12:
					b = 'PM'
				else:
					b = 'AM'




				#turns the start and end times into strings
				startHR = str(startHR)
				endHR = str(endHR)
				startMIN = str(startMIN)
				endMIN = str(endMIN)


				#adds it to the string of time
				if len(startHR) == 1:
					startHR = '0' + startHR
				if len(endHR) == 1:
					endHR = '0' + endHR

				if len(startMIN) == 1:
					startMIN = '0' + startMIN
				if len(endMIN) == 1:
					endMIN = '0' + endMIN


				#finalizes the time string
				time += startHR + ':' + startMIN + a + endHR + ':' + endMIN + b



				#adds the personal activity to the self.courses dictionary
				self.selectedmenu.insert(END, activitytype)
				self.selectedcourses.append(activitytype)
				self.courses[activitytype] = [Course('Personal Activity', activitytype, 0, time, 'Me!')]




				self.personalerror.configure(text='')
				self.starttime.delete(0, END)
				self.endtime.delete(0, END)
				self.activityname.delete(0, END)


			else:
				self.personalerror.configure(text='Wrong Format. Try Again.') #gives error message

		else:
			self.personalerror.configure(text='Wrong Format. Try Again.') #gives error message






			#gets all of the courses offered in the spring 2018 semester of cmu from the website
	def getcourses(self):


		#file18 = open('spring18updated.html', 'r')
		#data18 = file18.read()
		#print data18
		result = requests.get("https://enr-apps.as.cmu.edu/assets/SOC/sched_layout_spring.htm")
		soup18 = BeautifulSoup(result.text, 'lxml')


		#print soup18.beautify()
		#soup17 = BeautifulSoup(data17)

		lecturetime = ''
		springcourses = {}


		for course in soup18.find_all('tr'):
			courseinfo = course.find_all('td')


			if len(courseinfo) > 8:

				#checks if the line includes the title and number of the course
				if courseinfo[0].text.encode('utf-8').isdigit():

					#resets lecture variables since there might not be any lectures for a specific course
					lecture = False
					lecturetime = ''
					qatar = False

					#gets the course number and course name as strings
					coursenumber = courseinfo[0].text.encode('utf-8')
					coursename = courseinfo[1].text.encode('utf-8')

					#tries to calculate the number of units and gives unit values of -1 if it fails
					try:
						units = int(float(courseinfo[2].text.encode('utf-8')))
					except:
						units = -1



				#checks if the course/lecture is taking place in qatar
				if courseinfo[8].text.encode('utf-8') == 'Doha, Qatar':
					qatar = True

					try:
						professor = courseinfo[9].text.encode('utf-8')
					except:
						professor = ''


					#checks if there is a lecture involved and records the time
					if courseinfo[3].text.encode('utf-8')[:3] == 'Lec':
						lecture = True
						lecturetime = courseinfo[4].text.encode('utf-8')+courseinfo[5].text.encode('utf-8')+ courseinfo[6].text.encode('utf-8')


					#prints out the course if it is not a lecture but actual class time
					else:

						coursetime = courseinfo[4].text.encode('utf-8')+courseinfo[5].text.encode('utf-8')+ courseinfo[6].text.encode('utf-8')
						coursetime += ' ' + lecturetime

						if coursenumber == '15110':
							coursetime = 'UT' + courseinfo[4].text.encode('utf-8')+courseinfo[5].text.encode('utf-8')+ courseinfo[6].text.encode('utf-8')


						#criteria for adding a course to the dictionary of Courses
						#there must be a professor for it, it must have a definite number of units, and there must be a coursetime
						if len(professor) > 2 and units > 0 and len(coursetime) > 4 and qatar:


							#adds the course to the dictionary springcourses
							if coursenumber in springcourses:
								springcourses[coursenumber].append(Course(coursenumber, coursename, units, coursetime, professor))
							else:
								springcourses[coursenumber] = [Course(coursenumber, coursename, units, coursetime, professor)]


		return springcourses









#class to display the courseplan data
class DisplayResult():

	def __init__(self, courses, courseplan, totalunits, saved):

		#sets up the window layout
		self.master = Tk()
		self.master.title('View Course Plan')
		self.master.geometry('800x500')

		#sets up the given parameters and arguments
		self.totalunits = totalunits
		self.courses = courses
		self.courseplan = courseplan

		#calculates the units if this is coming from the server directly
		if saved:
			self.totalunits = 0
			for course in self.courseplan:
				self.totalunits += courses[course][0].units



		#SETS UP THE LAYOUT OF THE SCREEN
		Label(self.master, text='Pick a day of the week to view your schedule:').grid(row=0, column=0)


		if saved:
			Label(self.master, text='You will be taking ' + str(self.totalunits) + ' units.').grid(row=1, column=0)


		self.viewschedule = Listbox(self.master, exportselection=0, height=15, width=50)
		self.viewschedule.grid(row=1, column=1)



		self.Sunday = Button(self.master, text='Sunday', command=self.v_sunday, width=12)
		self.Sunday.grid(row=2, column=0, sticky='W')
		self.Monday = Button(self.master, text='Monday', command=self.v_monday, width=12)
		self.Monday.grid(row=3, column=0, sticky='W')
		self.Tuesday = Button(self.master, text='Tuesday', command=self.v_tuesday, width=12)
		self.Tuesday.grid(row=4, column=0, sticky='W')
		self.Wednesday = Button(self.master, text='Wednesday', command=self.v_wednesday, width=12)
		self.Wednesday.grid(row=5, column=0, sticky='W')
		self.Thursday = Button(self.master, text='Thursday', command=self.v_thursday, width=12)
		self.Thursday.grid(row=6, column=0, sticky='W')



		#ALLOWS THE USER TO SAVE THE COURSEPLAN IF IT HAS NOT BEEN SAVED YET
		if not saved:
			Label(self.master, text='Create a username to save your courseplan:').grid(row=2, column=1)
			self.username = Entry(self.master)
			self.username.grid(row=3, column=1)

			self.saveplan = Button(self.master, text='Save!', command=self.save_plan)
			self.saveplan.grid(row=4, column=1)

			self.saveerror = Label(self.master, text='')
			self.saveerror.grid(row=5,column=1)



		self.master.mainloop()




	#tries to login and kills the screen if wrong login
	#closes login screen and opens new main screen if login is correct


	def format_time_range(self, starttime, endtime):

		starttime = str(starttime)
		endtime = str(endtime)

		start = starttime[:-2] + ':' + starttime[-2:]
		end = endtime[:-2] + ':' + endtime[-2:]

		finalstr = start + ' - ' + end

		return [finalstr, int(starttime)]


	#SAVES THE COURSE PLAN BY ACCESSING THE SOCKET SERVER AND SAVING A File
	#THIS IS DONE THROUGH LOGGING IN AND CREATING A SOCKET CONNECTION
	def save_plan(self):
		a = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		a.connect(("86.36.35.17", 15112))

		login(a, 'monkey2', 'banana2') #logins into the server

		getMail(a) ##reads the file

		plans = open("savedplans.txt",'r')
		planlist = plans.readlines()
		plans.close()




		#THIS IS THE DICTIONARY OF ALL OF THE ENTRIES IN THE SAVEDPLANS.TXT FILE
		plandict = {}

		for x in planlist:

			courselist = x.split()
			if len(courselist) > 1:
				plandict[courselist[0]] = courselist[1:]


		sendplan = []


		for course in self.courseplan: #determines if the course is in self.courses and adds it to the courseplan
			if course.isdigit() and len(course) == 5:
				sendplan.append(course)

		plandict[self.username.get()] = sendplan

		returnplans = open("savedplans.txt","w")


		#tHIS GOES THOUGH EACH ENTRY AND ADDS IT BACK TO THE FILE


		for person in plandict:
			append1 = ''
			append1 += person
			for course in plandict[person]:
				append1 += ' ' + course
			returnplans.write(append1 + '\n')

		returnplans.close()

		sendFile(a, 'monkey2', 'savedplans.txt') #sends the newly updated file back to the servers



		a.close() ##closes the socket connection


#
#THE NEXT FIVE FUNCTIONS SET UP THE CALL FUNCTIONS FOR THE

#INDIVIDUAL  FIVE BUTTONS FOR THE DAYS OF THE WEEK FROM
#SUNDAY OT thursday
#
#
#tHEY EACH POPULATE THE LISTBOX FOR THEIR RESPECTIVE
#DAYS AND ORDER THE SCHEDULE OF THE DAY IN ORDER OF time
#they go the weekschedule class using the getmin and getmax functions to sort the courses
#and adds it to the courseplan in order when the corresponding button is pressed to the day
#
	def v_sunday(self):

		self.viewschedule.delete(0, END)

		display = {}

		for course in self.courseplan:

			begtime = self.courses[course][0].time.getmin('U')
			endtime = self.courses[course][0].time.getmax('U')

			if begtime != None and endtime != None:

				times = self.format_time_range(begtime, endtime)
				display[times[1]] = course + '     ' + times[0]

		for time in sorted(display.keys()):
			self.viewschedule.insert(END, display[time])



	def v_monday(self):

		self.viewschedule.delete(0, END)

		display = {}

		for course in self.courseplan:

			begtime = self.courses[course][0].time.getmin('M')
			endtime = self.courses[course][0].time.getmax('M')

			if begtime != None and endtime != None:

				times = self.format_time_range(begtime, endtime)
				display[times[1]] = course + '     ' + times[0]

		for time in sorted(display.keys()):
			self.viewschedule.insert(END, display[time])





	def v_tuesday(self):

		self.viewschedule.delete(0, END)

		display = {}

		for course in self.courseplan:

			begtime = self.courses[course][0].time.getmin('T')
			endtime = self.courses[course][0].time.getmax('T')

			if begtime != None and endtime != None:

				times = self.format_time_range(begtime, endtime)
				display[times[1]] = course + '     ' + times[0]

		for time in sorted(display.keys()):
			self.viewschedule.insert(END, display[time])




	def v_wednesday(self):

		self.viewschedule.delete(0, END)

		display = {}

		for course in self.courseplan:

			begtime = self.courses[course][0].time.getmin('W')
			endtime = self.courses[course][0].time.getmax('W')

			if begtime != None and endtime != None:

				times = self.format_time_range(begtime, endtime)
				display[times[1]] = course + '     ' + times[0]

		for time in sorted(display.keys()):
			self.viewschedule.insert(END, display[time])



	def v_thursday(self):

		self.viewschedule.delete(0, END)

		display = {}

		for course in self.courseplan:

			begtime = self.courses[course][0].time.getmin('R')
			endtime = self.courses[course][0].time.getmax('R')

			if begtime != None and endtime != None:

				times = self.format_time_range(begtime, endtime)
				display[times[1]] = course + '     ' + times[0]

		for time in sorted(display.keys()):
			self.viewschedule.insert(END, display[time])



#md5 HASH FUNCITON TO LOGIN INTO THE RAZAK SERVER
def login (q, username, password):

	#sends username
	q.send("LOGIN " + username + "\n")
	secret_code = q.recv(512).split()


	#combines the challenge string with the password
	message = password + secret_code[2]

	length_message = len(message)


	#creates initial MD5 block of 512 characters length
	block512 = message
	block512 += '1'
	block512 += (508-length_message) * '0'


	#adds the length of the string at the beginning of the block
	if length_message <10:
		block512 += '00' + str(length_message)
	elif length_message < 100:
		block512 += '0' + str(length_message)
	else:
		block512 + str(length_message)



	#Splits up the block of 512 length into 16 pieces and calculates the sum of the cahractetres ascii values
	#and adds each sum to the list M
	M = []
	for x in range(16):
		sumchar = 0
		for y in range(32):
			sumchar += ord(block512[y])
		M.append(sumchar)
		block512 = block512[32:]



	#Initializes the MD5 lsits s and K o be used in the algorithm
	s = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22]
	s += [5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20]
	s += [4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23]
	s += [6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]


	K = [ 0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee ]
	K += [ 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501 ]
	K += [ 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be ]
	K += [ 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821 ]
	K += [ 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa ]
	K += [ 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8 ]
	K += [ 0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed ]
	K += [ 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a ]
	K += [ 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c ]
	K += [ 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70 ]
	K += [ 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05 ]
	K += [ 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665 ]
	K += [ 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039 ]
	K += [ 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1 ]
	K += [ 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1 ]
	K += [ 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391 ]


	#initializes variables
	a0 = 0x67452301
	b0 = 0xefcdab89
	c0 = 0x98badcfe
	d0 = 0x10325476

	A = a0
	B = b0
	C = c0
	D = d0



	#MD5 algorithm which caluculates the hash value
	for i in range(64):
		if i<16:
			F = (B & C) | ((~B) & D)
			F = F & 0xFFFFFFFF
			g = i
		elif i<32:
			F = (D & B) | ((~D) & C)
			F = F & 0xFFFFFFFF
			g = (5*i + 1) % 16
		elif i<48:
			F = B ^ C ^ D
			F = F & 0xFFFFFFFF
			g = (3*i + 5) % 16
		else:
			F = C ^ (B | (~D))
			F = F & 0xFFFFFFFF
			g = (7*i) % 16


		dTemp = D
		D = C
		C = B
		B = B + leftrotate((A + F + K[i] + M[g]), s[i]) #final step of the MD5 - calls on helper function
		B = B & 0xFFFFFFFF
		A = dTemp




	a0 = (a0 +A) & 0xFFFFFFFF
	b0 = (b0 +B) & 0xFFFFFFFF
	c0 = (c0 +C) & 0xFFFFFFFF
	d0 = (d0 +D) & 0xFFFFFFFF


	#concatenates the four individual hash strings
	result = str(a0) + str(b0) + str(c0) + str(d0)




	q.send('LOGIN ' + username + ' ' + result + '\n')
	authentication = q.recv(512)


	#returns true for successful authentication or false for failed authentication
	return authentication[0] == "L"


#Used as the final step in the MD5 hash function, takes in two numbers x,c
def leftrotate (x,c):
	return (x<<c) & 0xFFFFFFFF | (x >> (32-c) & 0x7FFFFFFF >> (32-c))




#takes in a string to be sent to the server and returns the same string except with the size added on to the beginning
def addSize(string1):
	length = len(string1) + 6

	string1 = '@' + ('0'*(5-len(str(length)))) + str(length) + string1

	return string1




def getMail(s):

	#gets raw data from server for messages and files
	s.send('@rxmsg')
	size_msg = int(s.recv(6)[1:6])
	response = s.recv(size_msg)


	#turns the raw data into a list
	response_list = response.split('@')
	response_list = response_list[2:]

	#initilaizes list for messages and list for files
	messages = []
	files = []

	#gets all of the messeges and users as tuples
	for x in range(0, len(response_list), 3):
		if response_list[x] == 'msg':
			messages.append((response_list[x+1], response_list[x+2]))

	#gets all of the users and files if there were files sent
	if 'file' in response_list:
		file_loc = response_list.index('file')
		for x in range(file_loc,len(response_list), 4):

			#creates a new document with the filename and content
			a = open(response_list[x+2], 'w')
			a.write(response_list[x+3])
			a.close()



def sendFile(s, friend, filename):

	#opens file and reads it
	a = open(filename)
	file_content = a.read()
	a.close()

	#string to send
	string = '@sendfile@' + friend + '@' + filename + '@' +file_content


	#adds the size
	string = addSize(string)

	#sends the file string
	s.send(string)
	a = s.recv(512)[7:9]



#really the only line of code that technically runs in the main interface
start = WelcomeScreen()


#fin
