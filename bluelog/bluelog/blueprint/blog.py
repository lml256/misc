from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for, abort, make_response
from bluelog.models import Post, Category, Comment, Admin
from bluelog.forms import AdminCommentForm, CommentForm
from bluelog.extensions import db
from flask_login import current_user

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
	page = request.args.get('page', 1, type=int)
	per_page = current_app.config['BLUELOG_POST_PER_PAGE']
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
	posts = pagination.items
	return render_template('blog/index.html', pagination=pagination, posts=posts)


@blog_bp.route('/about')
def show_about():
	about = Admin.query.get(1).about
	return render_template('blog/about.html', about=about)


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
	# url_for可将任意查询字符串添加到url中，然后可以用request.args获取
	category = Category.query.get_or_404(category_id)
	page = request.args.get('page', 1, type=int)
	per_page = current_app.config['BLUELOG_POST_PER_PAGE']
	pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
	posts = pagination.items
	return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
	post = Post.query.get_or_404(post_id)
	page = request.args.get('page', 1, type=int)
	per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
	pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.asc()).paginate(page, per_page)
	comments = pagination.items

	if current_user.is_authenticated:
		form = AdminCommentForm()
		form.author.data = current_app.name
		form.email.data = current_app.config['BLUELOG_EMAIL']
		form.site.data = url_for('.index')
		from_admin = True
		reviewed = True
	else:
		form = CommentForm()
		from_admin = False
		reviewed = False

	if form.validate_on_submit():
		author = form.author.data
		email = form.email.data
		site = form.site.data
		body = form.body.data
		comment = Comment(author=author, email=email, site=site, body=body, from_admin=from_admin, post=post, reviewed=reviewed)
		replied_id = request.args.get('reply')
		if replied_id:
			replied_comment = Comment.query.get_or_404(replied_id)
			comment.replied = replied_comment
		db.session.add(comment)
		db.session.commit()
		flash("评论成功", "success")
		return redirect(url_for('.show_post', post_id=post_id))
	return render_template('blog/post.html', post=post, pagination=pagination, comments=comments, form=form)


@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	return redirect(
		url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + "#comment-form")


@blog_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
	if theme_name not in current_app.config['BLUELOG_THEMES'].keys():
		abort(404)
	response = make_response(redirect(url_for('.index')))
	response.set_cookie('theme', theme_name, max_age=30 * 24 * 60 * 60)
	return response
