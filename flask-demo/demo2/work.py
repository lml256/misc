from flask import render_template
from flask import request, flash
from flask import Blueprint, redirect, url_for
from demo2.db import get_db

app = Blueprint('work', __name__, url_prefix='/')


@app.route('/', methods=('GET', 'POST'))
def index():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None

		user = db.execute(
			'SELECT * FROM user WHERE username = ?', (username,)
		).fetchone()

		if not username:
			error = '请输入用户名'
		elif not password:
			error = '请输入密码'
		elif not user or password != user['password']:
			error = '密码错误'

		if error is None:
			return redirect(url_for('work.data'))
		flash(error)
	return render_template('index.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		if not username:
			error = '请输入用户名'
		elif not password:
			error = '请输入密码'
		elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
			error = '用户名已存在'

		if error is None:
			db.execute(
				'INSERT INTO user (username, password) VALUES (?, ?)',
				(username, password)
			)
			db.commit()
			return redirect(url_for('work.index'))

		flash(error)
	return render_template('register.html')


@app.route('/data', methods=('GET', 'POST'))
def data():
	if request.method == 'POST':
		username = request.form['username']
		id = request.form['id']
		chinese = request.form['chinese']
		math = request.form['math']
		english = request.form['english']
		physical = request.form['physical']
		error = None
		db = get_db()
		if not username or not id or not chinese or not math or not english or not physical:
			error = '输入不合法'
		if not error:
			try:
				db.execute(
					'INSERT INTO student (name, id, chinese, english, math, physical) VALUES (?, ?, ?, ?, ?, ?)',
					(username, id, chinese, math, english, physical)
				)
				db.commit()
				flash("添加成功")
				student = db.execute(
					'SELECT * FROM student'
				).fetchall()
				return render_template('data.html', student=student)
			except:
				db.close()
				error = '学号重复'
		flash(error)
	if request.method == 'GET':
		student = get_db().execute(
			'SELECT * FROM student'
		).fetchall()
		return render_template('data.html', student=student)
	return render_template('data.html')


@app.route('/<string:id>/delete', methods=('GET', 'POST'))
def delete(id):
	db = get_db()
	try:
		db.execute('DELETE FROM student WHERE id = ?', (id,))
		db.commit()
		flash('删除成功')
	except:
		db.close()
	return redirect(url_for('work.data'))


@app.route('/search', methods=('GET', 'POST'))
def search():
	if request.method == 'POST':
		id = request.form['id']
		student = get_db().execute(
			'SELECT * FROM student WHERE id = ?', (id,)
		).fetchall()
		return render_template('search.html', student=student)
	student = []
	return render_template('search.html', student=student)