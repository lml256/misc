from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
ckeditor = CKEditor()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # 当login_required验证失败时重定向的视图
login_manager.login_message_category = 'waring'  # 设置验证失败时显示的消息属性
login_manager.login_message = u'请先登陆'  # 警告消息

csrf = CSRFProtect()



@login_manager.user_loader
def load_user(user_id):
	from bluelog.models import Admin
	user = Admin.query.get(user_id)
	return user

