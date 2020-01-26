import os
from flask import Flask
from flask_bootstrap import Bootstrap


def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY="^*&*&JKHkd",
		DATABASE=os.path.join(app.instance_path, 'work.sqlite')
	)

	if test_config is None:
		# 使用 config.py 中的值来重载缺省配置，如果 config.py 存在的话。
		# 例如，当正式部署的时候，用于设置一个正式的 SECRET_KEY
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	from . import db
	db.init_app(app)

	Bootstrap(app)

	from . import work
	app.register_blueprint(work.bp)

	return app

