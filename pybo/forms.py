from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, EmailField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class QuestionForm(FlaskForm):
    subject = StringField('Title', validators=[DataRequired()])    #필수 값인 경우 DataRequied   (msg)
    content = TextAreaField('contents', validators=[DataRequired()])
    uploaded_img_file = FileField('image upload', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'gif'], 'image file only')])

class AnswerForm(FlaskForm):
    content = TextAreaField('contents', validators=[DataRequired('Contents are required fields.')])

class UserCreateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', 'Password is not matching')])
    password2 = PasswordField('Password check', validators= [DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])


class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])