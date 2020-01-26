import click
from sayhello import app
from sayhello import db
from sayhello.models import Message


@app.cli.command()
@click.option('--count', default=30, help='生成随机数据')  # 默认生成30条随机数据
def forge(count):
	from faker import Faker

	# 创建虚拟数据前，重建数据库
	db.drop_all()
	db.create_all()

	data = Faker()
	click.echo('Working..')
	for i in range(count):
		message = Message(
			name=data.name(),
			body=data.sentence(),
			timestamp=data.date_time_this_year()
		)
		db.session.add(message)
	db.session.commit()
	click.echo('Done..')