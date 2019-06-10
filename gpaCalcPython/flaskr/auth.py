import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from passlib.hash import sha256_crypt

from flaskr.db import get_db
# from flaskr.calc import index

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, sha256_crypt.hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username or password.'
        elif not sha256_crypt.verify(password, user['password']):
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('calc.viewClasses'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/changePassword', methods=('GET', 'POST'))
@login_required
def passwordReset():
    if request.method == 'POST':
        username = request.form['username']
        oldPass = request.form['oldPassword']
        newPass = request.form['newPassword']
        error = None
        # user = db.execute(
        #     'SELECT * FROM user WHERE username = ?', (username,)
        # ).fetchone()

        if newPass is None:
            error = 'Input a new password'
        else:
        # elif not sha256_crypt.verify(oldPass, user['password']):
        #     id = user['id']
            db = get_db()
            db.execute(
                'UPDATE user SET password = ?'
                ' WHERE id = ?',
                (sha256_crypt.hash(newPass), g.user['id'])
            )
            db.commit()
            return redirect(url_for('calc.index'))

        flash(error)

    return render_template('auth/changePassword.html')
	