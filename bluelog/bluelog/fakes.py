from bluelog.models import Admin, Category, Post, Comment, Link
from bluelog.extensions import db
from sqlalchemy.exc import IntegrityError
from faker import Faker
import random

fake = Faker()


def fake_admin():
	admin = Admin(
		username='admin',
		blog_title='Bluelog',
		blog_sub_title="No, I'm the real thing",
		name='Mima Kirigoe',
		about='Um, l, Mima Kirigoe, had a fun time as a member of CHAM...'
	)
	admin.set_password('helloflask')
	db.session.add(admin)
	db.session.commit()


def fake_categories(count=10):
	category = Category(name='Default')
	db.session.add(category)
	for i in range(count):
		category = Category(name=fake.word())
		db.session.add(category)
		try:
			db.session.commit()
		except IntegrityError:  # 如果标签已经定义过，进行回滚操作
			db.session.rollback()


def fake_posts(count=50):
	for i in range(count):
		post = Post(
			title=fake.sentence(),
			body=fake.text(2000),
			category=Category.query.get(random.randint(1, Category.query.count())),  # 为文章随机指定主题
			timestamp=fake.date_time_this_year()
		)
		db.session.add(post)
	db.session.commit()


def fake_comments(count=500):
	# 已经审核的评论
	for i in range(count):
		comment = Comment(
			author=fake.name(),
			email=fake.email(),
			site=fake.url(),
			body=fake.sentence(),
			timestamp=fake.date_time_this_year(),
			reviewed=True,
			post=Post.query.get(random.randint(1, Post.query.count()))  # 为评论随机指定所在的博客
		)
		db.session.add(comment)
	for i in range(int(count*0.1)):
		# 未审核的评论
		comment = Comment(
			author=fake.name(),
			email=fake.email(),
			site=fake.url(),
			body=fake.sentence(),
			timestamp=fake.date_time_this_year(),
			reviewed=False,
			post=Post.query.get(random.randint(1, Post.query.count()))
		)
		db.session.add(comment)

		# 管理员评论
		comment = Comment(
			author='Mima Kirigoe',
			email='mima@example.com',
			site='example.com',
			body=fake.sentence(),
			timestamp=fake.date_time_this_year(),
			from_admin=True,
			reviewed=True,
			post=Post.query.get(random.randint(1, Post.query.count()))
		)
		db.session.add(comment)
	# 评论的回复
	for i in range(int(count*0.1)):
		comment = Comment(
			author=fake.name(),
			email=fake.email(),
			site=fake.url(),
			body=fake.sentence(),
			timestamp=fake.date_time_this_year(),
			reviewed=True,
			replied=Comment.query.get(random.randint(1, Comment.query.count())),
			post=Post.query.get(random.randint(1, Post.query.count()))  # !
		)
		db.session.add(comment)
	db.session.commit()


def fake_links(count=5):
	for i in range(count):
		link = Link(
			name=fake.name(),
			url=fake.url(),
		)
		db.session.add(link)
	db.session.commit()
