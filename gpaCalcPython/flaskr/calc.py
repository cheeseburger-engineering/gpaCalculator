from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('calc', __name__)

@bp.route('/')
def index():
    db = get_db()
    return render_template('calc/index.html')

# Login view to see saved classes/grades
@bp.route('/accountInfo')
@login_required
def viewClasses():
    db = get_db()
    courses = get_db().execute(
        'SELECT p.id, classname, grade, credits, author_id, username'
        ' FROM class p JOIN user u ON p.author_id = u.id'
        ' WHERE u.id = ?',
        (g.user['id'],)
    ).fetchall()
    avg = getAvgGpa()
    if session.get('goal') == True:
        goal = session['goal']
    else:
        goal = 0
    return render_template('calc/view.html', courses=courses, avg=avg, goal=goal)
	
def getAvgGpa():
    db = get_db()
    gradeSum = get_db().execute(
        'SELECT SUM(grade*credits)'
        ' FROM class p JOIN user u ON p.author_id = u.id'
        ' WHERE u.id = ?',
        (g.user['id'],)
    ).fetchone()[0]
    creditSum = get_db().execute(
        'SELECT SUM(credits)'
        ' FROM class p JOIN user u ON p.author_id = u.id'
        ' WHERE u.id = ?',
        (g.user['id'],)
    ).fetchone()[0]
    if gradeSum:
        avg = let2GPA(perc2let(round(gradeSum / creditSum, 2)))
    else:
        avg = 0
    return avg
	
@bp.route('/getGoalInfo')
@login_required
def getGoalInfo():
    db = get_db()
    courses = get_db().execute(
        'SELECT p.id, classname, grade, credits, author_id, username'
        ' FROM class p JOIN user u ON p.author_id = u.id'
        ' WHERE u.id = ?',
        (g.user['id'],)
    ).fetchall()

    if request.method == 'POST':
        session['classname'] = request.form['classname']
        session['credits'] = request.form['credits']
        error = None
        session['goal'] = getGoalGpa(getAvgGpa(), session['credits'], courses)

        if error is not None:
            flash(error)
        else:
            session['goal'] = getGoalGpa(getAvgGpa(), session['credits'], courses)
            return redirect(url_for('calc.viewClasses'))
    return render_template('calc/goal.html')

# Function to determine grade necessary to maintain GPA
def getGoalGpa(goal, credit, courses):
    # Expected input is goal GPA (float), goalCourse (course object with attributes: letter grade (string) and credits (int)), and courses (list of course objects)
	totGrade = 0
	totCredits = 0
	for course in courses:
		totGrade += let2GPA(course.grade)
		totCredits += credits
	goalGrade = goal * (totCredits + goalCourse.credits) - totGrade
	return goalGrade

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        classname = request.form['classname']
        grade = request.form['grade']
        credits = request.form['credits']
        error = None

        if not classname:
            error = 'Class name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO class (classname, grade, credits, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (classname, grade, credits, g.user['id'])
            )
            db.commit()
            return redirect(url_for('calc.viewClasses'))

    return render_template('calc/create.html')

def get_class(id, check_author=True):
    course = get_db().execute(
        'SELECT p.id, classname, grade, credits, author_id, username'
        ' FROM class p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if course is None:
        abort(404, "Class id {0} doesn't exist.".format(id))

    if check_author and course['author_id'] != g.user['id']:
        abort(403)

    return course

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    course = get_class(id)

    if request.method == 'POST':
        classname = request.form['classname']
        grade = request.form['grade']
        credits = request.form['credits']
        error = None

        if not classname:
            error = 'Class name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE class SET classname = ?, grade = ?, credits = ?'
                ' WHERE id = ?',
                (classname, grade, credits, id)
            )
            db.commit()
            return redirect(url_for('calc.viewClasses'))

    return render_template('calc/update.html', course=course)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM class WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('calc.viewClasses'))

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
def perc2let(grade):
    # Expected input is grade (int/float)
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
    # Expected input is string representing letter grade
	return SCORE_MAP[letter]
	
# Function to calculate weighted GPA contribution for a course
def weighGPA(course):
    # Expect input is course object with attributes: letter grade (string) and credits (int)
	return let2GPA(course.grade)*course.credits

# Function to calculate overall GPA for a list of courses
def calcTotalGPA(courses):
    # Expected input is list of courses, each with attributes: letter grade (string) and credits (int)
	totGPA = 0
	for course in courses:
		totGPA += weighGPA(course)
	totGPA = totGPA / len(courses)
	return totGPA
	
# Fuctions below are more oriented toward manipulating the data for a use
# i.e. setting grades, setting course credit values, etc.
	
# Function to set grade for course based on input	
def setGrade(course, grade):
    # Expected input is course (course object with attributes: letter grade (string) and credits (int))
	if isinstance(grade, str):
		course.grade = grade
	else:
		course.grade = perc2let(grade)
		
def setCredit(course, credits):
    # Expected input is course (course object with attributes: letter grade (string) and credits (int)) and credits (list of course objects)
	course.credits = credits