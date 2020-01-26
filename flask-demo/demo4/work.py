from flask import Blueprint, flash, render_template, redirect, request, url_for
from demo4.db import get_db
bp = Blueprint('work', __name__, url_prefix="/")


@bp.route('/', methods=('GET', 'POST'))
def index():
	db = get_db()
	if request.method == 'POST':
		name = request.form['name']
		error = None
		if not name:
			error = "名字不可为空"
		if not error:
			books = db.execute(
				'SELECT * FROM book WHERE name = ?', (name, )
			).fetchall()
			if books:
				flash("查询成功")
				return render_template('index.html', books=books)
			else:
				flash("暂无此书")
				return render_template('index.html', books=[])
		flash(error)
	books = db.execute(
		'SELECT * FROM book'
	).fetchall()
	return render_template('index.html', books=books)


@bp.route('/add', methods=('GET', 'POST'))
def add():
	if request.method == 'POST':
		name = request.form['name']
		price = request.form['price']
		num = request.form['num']
		error = None
		if not name or not price or not num:
			error = "不合法的输入"
		if not error:
			db = get_db()
			db.execute(
				'INSERT INTO book (name, price, num) VALUES(?, ?, ?)', (name, price, num)
			)
			db.commit()
			flash("添加成功")
			return render_template('add.html')
		flash(error)
	return render_template('add.html')


@bp.route('/delete', methods=('GET', 'POST'))
def delete():
	if request.method == 'POST':
		name = request.form['name']
		db = get_db()
		error = None
		if not name:
			error = "不合法的输入"
		if not error:
			db.execute(
				'DELETE FROM book WHERE name = ?', (name,)
			)
			db.commit()
			flash("删除成功")
			return render_template('delete.html')
		flash(error)
	return render_template('delete.html')
