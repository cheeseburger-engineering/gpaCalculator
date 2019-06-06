# Dictionary to convert letter grade to GPA
SCORE_MAP = {'A' : 4.0,
			 'a' : 4.0,
			 'A-': 3.7,
			 'a-': 3.7,
			 'B+': 3.3,
			 'b+': 3.3,
			 'B' : 3.0,
			 'b' : 3.0,
			 'B-': 2.7,
			 'b-': 2.7,
			 'C+': 2.3,
			 'c+': 2.3,
			 'C' : 2.0,
			 'c' : 2.0,
			 'C-': 1.7,
			 'c-': 1.7,
			 'D+': 1.3,
			 'd+': 1.3,
			 'D' : 1.0,
			 'd' : 1.0,
			 'F' : 0.0,
			 'f' : 0.0}

# Function to convert percentage grade to letter
def perc2let(grade)
	if grade > 92:
		let_grade = 'A'
	elif grade > 89:
		let_grade = 'A-'
	elif grade > 86:
		let_grade = 'B+'
	elif grade > 82:
		let_grade = 'B'
	elif grade > 79:
		let_grade = 'B-'
	elif grade > 76:
		let_grade = 'C+'
	elif grade > 72:
		let_grade = 'C'
	elif grade > 69:
		let_grade = 'C-'
	elif grade > 66:
		let_grade = 'D+'
	elif grade > 64:
		let_grade = 'D'
	else:
		let_grade = 'F'
	
	return let_grade

# Function to convert letter grade to GPA
def let2GPA(letter):
	return SCORE_MAP[letter]
	
# Function to calculate weighted GPA contribution for a course
def weighGPA(course):
	return let2GPA(course.grade)*course.credits

# Function to calculate overall GPA for a list of courses
def calcTotalGPA(courses):
	totGPA = 0
	for course in courses:
		totGPA += weighGPA(course)
	totGPA = totGPA / len(courses)
	return totGPA

# Function to determine grade necessary to maintain GPA
def getGoal(goal, goalCourse, courses)
	totGrade = 0
	totCredits = 0
	for course in courses:
		totGrade += let2GPA(course.grade)
		totCredits += course.credits
	goalGrade = goal * (totCredits + goalCourse.credits) - totGrade
	return goalGrade
	
# Fuctions below are more oriented toward manipulating the data for a use
# i.e. setting grades, setting course credit values, etc.
	
# Function to set grade for course based on input	
def setGrade(course, grade):
	if isinstance(grade, str):
		course.grade = grade
	else:
		course.grade = perc2let(grade)
		
def setCredit(course, credits):
	course.credits = credits