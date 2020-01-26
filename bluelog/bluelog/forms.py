from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, ValidationError, TextAreaField, HiddenField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Length, Email, Optional, URL
from bluelog.models import Category


class LoginFrom(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
	password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
	remember = BooleanField('Remember me')
	submit = SubmitField('Log in')


class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
	category = SelectField('Category', coerce=int, default=1)
	body = CKEditorField('Body', validators=[DataRequired()])
	submit = SubmitField()

	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		self.category.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
	submit = SubmitField()

	def validate_name(self, field):
		if Category.query.filter_by(name=field.data).first():
			raise ValidationError('Name already in use.')


class CommentForm(FlaskForm):
	author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
	email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 255)])
	site = StringField('Site', validators=[Optional(), URL(), Length(0, 255)])
	body = TextAreaField('Comment', validators=[DataRequired()])
	submit = SubmitField()


class AdminCommentForm(CommentForm):
	author = HiddenField()
	email = HiddenField()
	site = HiddenField()


class LinkForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
	link = StringField('Link', validators=[DataRequired(), Length(1, 255)])
	submit = SubmitField()


class SettingForm(FlaskForm):
	blog_title = StringField('Blog Title', validators=[Length(0, 60)])
	blog_sub_title = StringField('Blog Sub Title', validators=[Length(0, 100)])
	name = StringField('Name', validators=[Length(0, 30)])
	about = TextAreaField('About')
	submit = SubmitField()


class UserInfoForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
	password = PasswordField('Password', validators=[DataRequired(), Length(8, 200)])
	submit = SubmitField()
