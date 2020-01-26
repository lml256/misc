from flask import Blueprint, render_template, request, current_app, \
	flash, redirect, url_for
from flask_login import login_required, logout_user
from bluelog.models import Post, Category, Comment, Link, Admin
from bluelog.forms import PostForm, CategoryForm, LinkForm, SettingForm, UserInfoForm
from bluelog.extensions import db
from bluelog.utils import redirect_back

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		title = form.title.data
		body = form.body.data
		category = Category.query.get(form.category.data)
		post = Post(title=title, body=body, category=category)
		db.session.add(post)
		db.session.commit()
		flash('Post created.', 'success')
		return redirect(url_for('blog.show_post', post_id=post.id))
	return render_template('admin/new_post.html', form=form)


@admin_bp.route('/new_category', methods=['GET', 'POST'])
@login_required
def new_category():
	form = CategoryForm()
	if form.validate_on_submit():
		name = form.name.data
		category = Category(name=name)
		db.session.add(category)
		db.session.commit()
		flash('Add Successful', 'success')
		return redirect(url_for('.manage_category'))
	return render_template('admin/new_category.html', form=form)


@admin_bp.route('/new_link', methods=['GET', 'POST'])
@login_required
def new_link():
	form = LinkForm()
	if form.validate_on_submit():
		name = form.name.data
		url = form.link.data
		link = Link(name=name, url=url)
		db.session.add(link)
		db.session.commit()
		flash("Add link successful", 'success')
		return render_template('admin/new_link.html', form=form)
	return render_template('admin/new_link.html', form=form)


@admin_bp.route('/manage_post')
@login_required
def manage_post():
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE'])
	posts = pagination.items
	return render_template('admin/manage_post.html', pagination=pagination, posts=posts)


@admin_bp.route('/manage_category/manage')
@login_required
def manage_category():
	return render_template('admin/manage_category.html')


@admin_bp.route('/manage_comment')
@login_required
def manage_comment():
	filter_rule = request.args.get('filter', 'all')
	page = request.args.get('page', 1, type=int)
	per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
	if filter_rule == 'unread':
		filter_comment = Comment.query.filter_by(reviewed=False)
	elif filter_rule == 'read':
		filter_comment = Comment.query.filter_by(reviewed=True)
	elif filter_rule == 'admin':
		filter_comment = Comment.query.filter_by(from_admin=True)
	else:
		filter_comment = Comment.query
	pagination = filter_comment.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
	comments = pagination.items
	return render_template('admin/manage_comment.html', comments=comments, pagination=pagination)


@admin_bp.route('/manage_link')
def manage_link():
	links = Link.query.order_by(Link.name.desc()).all()
	print(links)
	for link in links:
		print(link.name + " " + link.url)
	return render_template('admin/manage_link.html', links=links)


@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
	form = PostForm()
	post = Post.query.get_or_404(post_id)
	if form.validate_on_submit():
		post.title = form.title.data
		post.body = form.body.data
		post.category = Category.query.get(form.category.data)
		db.session.commit()
		flash('Post updated.', 'success')
		return redirect(url_for('blog.show_post', post_id=post.id))
	form.title.data = post.title
	form.body.data = post.body
	form.category.data = post.category_id
	return render_template('admin/edit_post.html', form=form)


@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
	category = Category.query.get_or_404(category_id)
	form = CategoryForm()
	if category_id == 1:
		flash('You can not edit default category.', 'waring')
		return redirect(url_for('.manage_category'))
	if form.validate_on_submit():
		category.name = form.name.data
		db.session.commit()
		flash('Change category successful.', 'success')
		return redirect(url_for('.manage_category'))
	form.name.data = category.name
	return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/link/<int:link_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_link(link_id):
	form = LinkForm()
	link = Link.query.get_or_404(link_id)
	if form.validate_on_submit():
		link.name = form.name.data
		link.url = form.link.data
		db.session.commit()
		flash("Change successful", 'success')
		return render_template('admin/edit_link.html', form=form)
	form.name.data = link.name
	form.link.data = link.url
	return render_template('admin/edit_link.html', form=form)


@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	db.session.delete(post)
	db.session.commit()
	flash('Post deleted.', 'success')
	return redirect_back()


@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	db.session.delete(comment)
	db.session.commit()
	flash('Delete successful.', 'success')
	return redirect_back()


@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
	category = Category.query.get_or_404(category_id)
	if category.id == 1:
		flash("You can not delete default category", 'waring')
		return redirect_back(url_for('admin.manage_category'))
	category.delete()
	flash('Category deleted.', 'success')
	return redirect(url_for('.manage_category'))


@admin_bp.route('/link/<int:link_id>/delete', methods=['POST'])
@login_required
def delete_link(link_id):
	link = Link.query.get_or_404(link_id)
	db.session.delete(link)
	db.session.commit()
	flash('Delete successful', 'success')
	return redirect_back()


@admin_bp.route('/set_comment/<int:post_id>', methods=['POST'])
@login_required
def set_comment(post_id):
	post = Post.query.get_or_404(post_id)
	post.can_comment = not post.can_comment
	flash('Comment disabled.', 'info')
	db.session.commit()
	return redirect(url_for('blog.show_post', post_id=post_id))


@admin_bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
@login_required
def approve_comment(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	comment.reviewed = True
	db.session.commit()
	flash('Comment published', 'success')
	return redirect_back()


@admin_bp.route('/settings/<int:setting_id>', methods=['GET', 'POST'])
@admin_bp.route('/settings')
@login_required
def settings(setting_id=0):
	form = SettingForm()
	user = UserInfoForm()
	admin = Admin.query.get_or_404(1)
	if setting_id == 1 and form.validate_on_submit():
		admin.blog_title = form.blog_title.data
		admin.blog_sub_title = form.blog_sub_title.data
		admin.name = form.name.data
		admin.about = form.about.data
		db.session.commit()
		flash("Change successful", 'success')
		return redirect(url_for('.settings'))

	if setting_id == 2 and user.validate_on_submit():
		admin.username = user.username.data
		admin.set_password(user.password.data)
		db.session.commit()
		flash("Change successful, please login again", 'success')
		logout_user()
		return redirect(url_for('.settings'))

	form.blog_title.data = admin.blog_title
	form.blog_sub_title.data = admin.blog_sub_title
	form.name.data = admin.name
	form.about.data = admin.about
	user.username.data = admin.username
	return render_template('admin/settings.html', form=form, user=user)
