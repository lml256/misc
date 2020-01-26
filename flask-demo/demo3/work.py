from flask import Blueprint, flash, render_template, redirect, request, url_for
from demo3.db import get_db
bp = Blueprint('work', __name__, url_prefix="/")


@bp.route('/')
def index():
	blogs = get_db().execute(
		'SELECT * FROM blog'
	).fetchall()
	return render_template('index.html', blogs=blogs)


@bp.route('/add', methods=('GET', 'POST'))
def add():
	if request.method == 'POST':
		title = request.form['title']
		blog = request.form['blog']
		db = get_db()
		error = None
		if not title:
			error = "标题不可为空"
		if not error:
			db.execute(
				'INSERT INTO blog (title, blog) VALUES(?, ?)', (title, blog)
			)
			db.commit()
			flash("添加成功")
			return render_template('add.html')
		flash(error)
	return render_template('add.html')


@bp.route('<int:id>/update', methods=('GET', 'POST'))
def update(id):
	if request.method == 'POST':
		title = request.form['title']
		blog = request.form['blog']
		db = get_db()
		error = None
		if not title:
			error = "标题不可为空"
		if not error:
			db.execute(
				'UPDATE blog SET title = ?, blog = ? WHERE id = ?', (title, blog, id)
			)
			db.commit()
			flash("修改成功")
			blog_t = db.execute(
				'SELECT * FROM blog WhERE id = ?', (id,)
			).fetchone()
			return render_template('update.html', blog=blog_t)
		flash(error)
	blog_t = get_db().execute(
		'SELECT * FROM blog WhERE id = ?', (id,)
	).fetchone()
	return render_template('update.html', blog=blog_t)


@bp.route('<int:id>/delete')
def delete(id):
	db = get_db()
	db.execute(
		'DELETE FROM blog WHERE id = ?', (id,)
	)
	db.commit()
	return redirect(url_for('work.index'))
