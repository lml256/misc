from flask import flash, redirect, url_for, render_template
from sayhello import app, db
from sayhello.models import Message
from sayhello.forms import HelloForm


@app.route('/', methods=['GET', 'POST'])
def index():
	# 以时间戳的降序进行查询
	messages = Message.query.order_by(Message.timestamp.desc()).all()  # 查询
	form = HelloForm()
	if form.validate_on_submit():
		name = form.name.data
		body = form.body.data
		message = Message(body=body, name=name)  # 创建记录
		db.session.add(message)
		db.session.commit()
		flash("创建成功")
		return redirect(url_for('index'))
	return render_template('index.html', form=form, messages=messages)