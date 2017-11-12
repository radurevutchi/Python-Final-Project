import requests
from bs4 import BeautifulSoup


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


		printstr = ''

		for x in self.days.keys():
			printstr += x + str(self.days[x][0]) + str(self.days[x][-1]) + '\n'

		return printstr


















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












	def __str__(self):

		return self.time



















spring18 = requests.get("https://enr-apps.as.cmu.edu/assets/SOC/sched_layout_spring.htm")
#fall17 = requests.get('https://enr-apps.as.cmu.edu/assets/SOC/sched_layout_fall.htm')

data18 = spring18.text
#data17 = fall17.text

soup18 = BeautifulSoup(data18, 'lxml')
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






#number is the course number in spring courses
for number in springcourses:

	#times is course object for a specific time
	print number, springcourses[number][0].name




print

choices = []

print 'Please enter your first choice course: '
choiceinput = raw_input()
print
while choiceinput not in springcourses:
	print 'Sorry, that course is not available.'
	print 'Please enter your first choice course:'
	choiceinput = raw_input()
	print
choices.append(choiceinput)

print 'Would you like to add another course? [y/n]'

another = raw_input()
print

while another not in ['y','n']:
	print 'Sorry that is not a valid input.'
	print 'Would you like to add another course? [y/n]'
	another = raw_input()
	print











while another == 'y':

	print 'Please enter your next favorite course: '
	choiceinput = raw_input()
	print

	while choiceinput not in springcourses:
		print 'Sorry, that course is not available.'
		print 'Please enter your next favorite course:'
		choiceinput = raw_input()
		print
	choices.append(choiceinput)




	print 'Would you like to add another course? [y/n]'
	another = raw_input()
	print

	while another not in ['y','n']:
		print 'Sorry that is not a valid input.'
		print 'Would you like to add another course? [y/n]'
		another = raw_input()
		print





'''
print
print 'What is the maximum number of units that you will take?'


maxunits = raw_input()
print

while not maxunits.isdigit():
	print 'Sorry that is not a valid integer.'
	print 'What is the maximum number of units that you will take?'
	maxunits = raw_input()
	print
'''

courseplan = []

courseplan.append(choices[0])

choices = choices[1:]


for x in choices:
	conflict = False

	for y in courseplan:
		if springcourses[x][0].interferes(springcourses[y][0]):
			conflict = True

	if not conflict:
		courseplan.append(x)


print 'This is the most ideal course plan for you!'
print courseplan











#fin
