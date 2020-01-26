from flask import render_template
from flask import request, flash
from flask import Blueprint
from demo1.db import get_db

bp = Blueprint('work', __name__, url_prefix='/')


@bp.route('/')
def hello_world():
	return render_template('hello.html')


@bp.route('/book', methods=['GET', 'POST'])
def book():
	if request.method == 'POST':
		bookname = request.form['bookname']
		localbook = request.form['localbook']
		borrow = request.form['borrow']
		error = None
		db = get_db()

		if not bookname:
			error = "请输入书名"
		elif not localbook:
			error = "请输入在馆图书数量"
		elif not borrow:
			error = "请输入已借阅数量"

		if not error:
			db.execute(
				'INSERT INTO lib (bookname, localbook, borrow) VALUES (?, ?, ?)',
				(bookname, localbook, borrow)
			)
			db.commit()
			flash("存储成功")
			return render_template('book.html')
		flash(error)
	return render_template('book.html')


@bp.route('/add', methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		bookname = request.form['bookname']
		db = get_db()
		if bookname:
			book = db.execute(
				'SELECT * FROM lib WHERE bookname = ?', (bookname,)
			).fetchall()
		else:
			book = db.execute(
				'SELECT * FROM lib',
			).fetchall()
		print(book)
		return render_template('add.html', boollist=book)
	return render_template('add.html')

