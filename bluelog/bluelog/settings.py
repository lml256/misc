import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 得到项目根目录的绝对路径


class BaseConfig(object):
	SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')  # 先从环境变量中获取密钥，获取不到为secret key

	SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不追踪对象的修改

	MAIL_SERVER = os.getenv('MAIL_SERVER')
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = os.getenv('MAIL_USERNAME')
	MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
	MAIL_DEFAULT_SENDER = ('Bluelog Admin', MAIL_USERNAME)
	BLUELOG_EMAIL = os.getenv('BLUELOG_EMAIL')
	BLUELOG_POST_PER_PAGE = 10
	BLUELOG_MANAGE_POST_PER_PAGE = 15
	BLUELOG_COMMENT_PER_PAGE = 15
	BLUELOG_THEMES = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan'}


class DevelopmentConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
	TESTING = True
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'


class ProductionConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data.db'))


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig
}