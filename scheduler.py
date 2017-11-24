import requests
from bs4 import BeautifulSoup
from Tkinter import *


'''
Courses that won't be included in the course selection:

- Ones that don't have a definite number of units assigned to them
- Ones that don't have a time assigned to them yet

'''






class WeekSchedule:

	def __init__(self, time):

		self.time = time
		self.days = {}
		self.days['U'] = []
		self.days['M'] = []
		self.days['T'] = []
		self.days['W'] = []
		self.days['R'] = []
		self.raw_times = self.time.split()


		self.fillDays()



	def fillDays(self):


		#Goes through each of the class hours of the course and adds to the dictionary self.days
		for lectures in self.raw_times:
			hours = lectures[-14:]
			weekdays = lectures[:-14]

			range_hours = self.toMilitaryTime(hours)


			#For each day of the week where there are classes, the range of military time will be added
			for a in range(len(weekdays)):

				self.days[weekdays[a]] += range(range_hours[0], range_hours[1])



	#converts the string in form ##:##@M##:##@M to military time and returns the beginning and end mlitary time
	def toMilitaryTime(self, normaltime):

		beg = normaltime[:7]
		end = normaltime[7:]

		begrange = int(beg[:2]) * 100

		begrange += int(beg[3:5])

		if beg[5:7] == 'PM' and int(beg[:2]) !=12:
			begrange += 1200


		endrange = int(end[:2]) * 100

		endrange += int(end[3:5])

		if end[5:7] == 'PM' and int(end[:2]) !=12:
			endrange += 1200


		return [begrange, endrange]


	def __str__(self):

		print self.days








class Course:

	def __init__(self, number, name, units, time, professor):

		self.number = number
		self.name = name
		self.units = units
		self.time = WeekSchedule(time)#time
		self.professor = professor


	def interferes(self, othercourse):

		conflicts = False
		currenttime = []
		othertime = []

		for x in ['U','M','T','W','R']:

			currenttime = set(self.time.days[x])
			othertime = set(othercourse.time.days[x])

			if len(list(currenttime & othertime)) > 5:
				return True


		return False







class WelcomeScreen():

	def __init__(self):

		#sets up the window layout
		self.master = Tk()
		self.master.title('CMU Course Scheduler')
		self.master.geometry('400x400')


		#sets the button to try login information, calls the function within this class
		self.retrieveButton = Button(self.master,text='Create New Schedule', command = self.create_main_window).grid(row=1, column=1)
		self.newButton = Button(self.master,text='Retrieve Saved Schedule', command = self.get_saved_schedule).grid(row=1, column=2)


		self.master.mainloop()




	#tries to login and kills the screen if wrong login
	#closes login screen and opens new main screen if login is correct
	def create_main_window(self):
		self.master.destroy()

		newschedule = CreateSchedule()


	#function to close the window.
	def get_saved_schedule(self):
		print 'saved'







class CreateSchedule():

	def __init__(self):

		#sets up the window layout

		self.maxunits = 0
		self.selectedunits = 0

		self.courses = self.getcourses()


		self.master = Tk()
		self.master.title('CMU Course Scheduler')
		self.master.geometry('900x600')




		Label(self.master, text='Pick the courses you want to take in order of favorites!').grid(row=0, column=0)
		self.coursemenu = Listbox(self.master, exportselection=0, height=20, width=50)
		self.coursemenu.grid(row=1, column=0)

		self.addcourse = Button(self.master, text='Pick Course', command=self.add_course)
		self.addcourse.grid(row=2, column=0)


		Label(self.master, text='Activity Name:').grid(row=3, column=0, sticky="W")
		self.activityname = Entry(self.master)
		self.activityname.grid(row=3, column=0)

		Label(self.master, text='From (hh:mm):').grid(row=4, column=0, sticky="W")
		self.starttime = Entry(self.master)
		self.starttime.grid(row=4, column=0)


		Label(self.master, text='To (hh:mm):').grid(row=5, column=0, sticky="W")
		self.endtime = Entry(self.master)
		self.endtime.grid(row=5, column=0)

		self.addactivity = Button(self.master, text='Add Personal Activity', command=self.add_personal_activity)
		self.addactivity.grid(row=6, column=0)

		self.personalerror = Label(self.master, text='')
		self.personalerror.grid(row=7,column=0)


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
		self.sunday.grid(row=8, column=0, sticky="W")
		self.monday.grid(row=9, column=0, sticky="W")
		self.tuesday.grid(row=10, column=0, sticky="W")
		self.wednesday.grid(row=11, column=0, sticky="W")
		self.thursday.grid(row=12, column=0, sticky="W")








		Label(self.master, text='Selected courses starting from the first choice:').grid(row=0, column=1)
		self.selectedmenu = Listbox(self.master, exportselection=0, height=10, width=50)
		self.selectedmenu.grid(row=1, column=1)

		self.resetcourses = Button(self.master, text='Reset', command=self.reset_selection)
		self.resetcourses.grid(row=2, column=1)


		self.unitslabel = Label(self.master, text='Units Selected: 0')
		self.unitslabel.grid(row=3, column = 1)

		self.resetcourses = Button(self.master, text='Calculate Course Plan!', command=self.get_course_plan)
		self.resetcourses.grid(row=4, column=1)

		self.calculateerror = Label(self.master, text='')
		self.calculateerror.grid(row=5, column = 1)


		self.sortedcourses = []
		self.personaltimes = ''
		self.selectedcourses = []

		self.sort_courses()
		self.update_courses()




		self.master.mainloop()




	#tries to login and kills the screen if wrong login
	#closes login screen and opens new main screen if login is correct

	def sort_courses(self):

		self.sortedcourses = map(lambda x: int(x), self.courses.keys())
		self.sortedcourses = sorted(self.sortedcourses)
		self.sortedcourses = map(lambda x: str(x), self.sortedcourses)


		for a in range(len(self.sortedcourses)):
			if len(self.sortedcourses[a]) == 4:
				self.sortedcourses[a] = '0' + self.sortedcourses[a]






	def update_courses(self):


		#updates list of courses to select from
		self.coursemenu.delete(0, END)
		for thing in self.sortedcourses:
			if thing not in map(lambda x: x[:5], self.selectedcourses):
				self.coursemenu.insert(END, thing + '  ' + self.courses[thing][0].name)




	def add_course(self):

		selection = self.coursemenu.curselection()
		if selection != (): #if a course is selected
			self.selectedcourses.append(self.coursemenu.get(selection[0])[:5])
			self.selectedmenu.insert(END, self.coursemenu.get(selection[0]))

			coursenumber = self.coursemenu.get(selection[0])[:5]
			units = self.courses[coursenumber][0].units
			self.selectedunits += units

			self.unitslabel.configure(text='Units Selected: ' + str(self.selectedunits))
			self.calculateerror.configure(text='')


		self.update_courses()




	def reset_selection(self):

		self.unitslabel.configure(text='Units Selected: 0')
		self.selectedmenu.delete(0, END)
		self.selectedcourses = []
		self.selectedunits = 0

		self.update_courses()



	def get_course_plan(self):

		courseplan = []

		if len(self.selectedcourses) > 0:

			courseplan.append(self.selectedcourses[0])
			self.selectedcourses = self.selectedcourses[1:]



			for x in self.selectedcourses:
				conflict = False

				for y in courseplan:


					if self.courses[x][0].interferes(self.courses[y][0]):
						conflict = True

				if not conflict:
					courseplan.append(x)


			print courseplan

		else:
			self.calculateerror.configure(text='You did not select any courses yet!')
		self.unitslabel.configure(text='Units Selected: 0')
		self.selectedmenu.delete(0, END)
		self.selectedcourses = []
		self.selectedunits = 0
		self.update_courses()







	def add_personal_activity(self):


		start = self.starttime.get()
		end = self.endtime.get()
		activitytype = self.activityname.get()

		days = {}
		days['U'] = self.var1.get()
		days['M'] = self.var2.get()
		days['T'] = self.var3.get()
		days['W'] = self.var4.get()
		days['R'] = self.var5.get()



		if len(start) == 5 and len(end) == 5 and start[0:2].isdigit() and start[3:5].isdigit() and end[0:2].isdigit() and end[3:5].isdigit() and start[2] == ':' and end[2] == ":" and activitytype:

			startHR = int(start[:2])
			startMIN = int(start[3:5])
			endHR = int(end[:2])
			endMIN = int(end[3:5])

			if startHR < 24 and endHR < 24 and startMIN < 60 and endMIN < 60 and reduce(lambda x,y: x+y, days.values()) != 0:


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




				startHR = str(startHR)
				endHR = str(endHR)
				startMIN = str(startMIN)
				endMIN = str(endMIN)



				if len(startHR) == 1:
					startHR = '0' + startHR
				if len(endHR) == 1:
					endHR = '0' + endHR

				if len(startMIN) == 1:
					startMIN = '0' + startMIN
				if len(endMIN) == 1:
					endMIN = '0' + endMIN


				time += startHR + ':' + startMIN + a + endHR + ':' + endMIN + b



				self.selectedmenu.insert(END, activitytype)
				self.selectedcourses.append(activitytype)
				self.courses[activitytype] = [Course('Personal Activity', activitytype, 0, time, 'Me!')]




				self.personalerror.configure(text='')
				self.starttime.delete(0, END)
				self.endtime.delete(0, END)
				self.activityname.delete(0, END)


			else:
				self.personalerror.configure(text='Wrong Format. Try Again.')

		else:
			self.personalerror.configure(text='Wrong Format. Try Again.')







	def getcourses(self):


		file18 = open('spring18updated.html', 'r')
		data18 = file18.read()
		#print data18

		soup18 = BeautifulSoup(data18, 'lxml')

		#print soup18.beautify()
		#soup17 = BeautifulSoup(data17)

		lecturetime = ''
		springcourses = {}


		for course in soup18.find_all('tr'):
			courseinfo = course.find_all('td')


			if len(courseinfo) >8:

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





class DisplayResult():

	def __init__(self, courses, courseplan):

		#sets up the window layout
		self.master = Tk()
		self.master.title('View Course Plan')
		self.master.geometry('800x400')



		Label(self.master, text='Pick a day of the week to view your schedule:').grid(row=0, column=0)



		self.viewschedule = Listbox(self.master, exportselection=0, height=10, width=50)
		self.viewschedule.grid(row=1, column=2)



		self.Sunday = Button(self.master, text='Sunday', command=self.v_sunday)
		self.Sunday.grid(row=1, column=0)
		self.Monday = Button(self.master, text='Monday', command=self.v_monday)
		self.Monday.grid(row=2, column=0)
		self.Tuesday = Button(self.master, text='Tuesday', command=self.v_tuesday)
		self.Tuesday.grid(row=3, column=0)
		self.Wednesday = Button(self.master, text='Wednesday', command=self.v_wednesday)
		self.Wednesday.grid(row=4, column=0)
		self.Thursday = Button(self.master, text='Thursday', command=self.v_thursday)
		self.Thursday.grid(row=5, column=0)


		Label(self.master, text='Create a username to save your courseplan:').grid(row=6, column=0)
		self.username = Entry(self.master)
		self.username.grid(row=5, column=0)


		self.saveplan = Button(self.master, text='Save!', command=self.add_personal_activity)
		self.addactivity.grid(row=6, column=0)

		self.saveerror = Label(self.master, text='')
		self.saveerror.grid(row=7,column=0)


		self.master.mainloop()




	#tries to login and kills the screen if wrong login
	#closes login screen and opens new main screen if login is correct
	def create_main_window(self):
		self.master.destroy()

		newschedule = CreateSchedule()


	#function to close the window.
	def get_saved_schedule(self):
		print 'saved'





start = WelcomeScreen()


#fin
