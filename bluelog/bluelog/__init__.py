import os
from flask import Flask, render_template, request, jsonify
from bluelog.blueprint.blog import blog_bp
from bluelog.blueprint.auth import auth_bp
from bluelog.blueprint.admin import admin_bp
from bluelog.blueprint.editor import editor_bp
from bluelog.settings import config
from bluelog.extensions import bootstrap, db, moment, ckeditor, login_manager, csrf
from bluelog.models import Admin, Category, Comment
from flask_wtf.csrf import CSRFError
from flask_login import current_user
from flask_cors import CORS
import click


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_blueprint(app)  # 注册蓝图
    register_extensions(app)  # 注册扩展
    register_template_context(app)  # 创建模板上下文
    register_commands(app)
    register_errors(app)

    @app.route('/test')
    def test():
        return '<h1>Hello</h1>'
    CORS(app)
    return app


def register_blueprint(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(editor_bp, url_prefix='/editor')


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    csrf.exempt(editor_bp)


def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10)
    @click.option('--post', default=50)
    @click.option('--comment', default=500)
    def forge(category, post, comment):
        from bluelog.fakes import fake_admin, fake_categories, fake_posts, fake_comments, fake_links

        click.echo('Drop database...')
        db.drop_all()
        db.create_all()

        click.echo('create new data...')
        fake_admin()
        fake_categories(category)
        fake_posts(post)
        fake_comments(comment)
        fake_links()
        click.echo('Done...')

    @app.cli.command()
    @click.option('--username', prompt=True, help='help message')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='help message')
    def init(username, password):
        click.echo("正在初始化")
        db.create_all()

        admin = Admin.query.first()
        if admin:
            click.echo("用户名已存在，正在更新")
            admin.username = username
            admin.set_password(password)
        else:
            click.echo("正在创建管理员账户")
            admin = Admin()
            admin.username = username
            admin.blog_title = 'Bluelog'
            admin.blog_sub_title = 'Blog Title'
            admin.name = 'Admin'
            admin.about = 'about'
            admin.set_password(password)
            db.session.add(admin)
        category = Category.query.first()
        if category is None:
            click.echo("创建默认类型")
            category = Category(name='Default')
            db.session.add(category)
        db.session.commit()
        click.echo('完成')


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()

        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None

        return dict(admin=admin, categories=categories, unread_comments=unread_comments)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('error/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('error/400.html', description=e.discription), 400
