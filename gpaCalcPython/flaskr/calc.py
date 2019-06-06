from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
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
    posts = get_db().execute(
        'SELECT p.id, classname, grade, credits, author_id, username'
        ' FROM class p JOIN user u ON p.author_id = u.id'
        ' WHERE u.id = ?',
        (g.user['id'],)
    ).fetchall()
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
    avg = round(gradeSum / creditSum, 2)
    return render_template('calc/view.html', posts=posts, avg=avg)

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

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, classname, grade, credits, author_id, username'
        ' FROM class p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

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

    return render_template('calc/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM class WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('calc.viewClasses'))

