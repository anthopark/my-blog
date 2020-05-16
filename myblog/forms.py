from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField,
                     SubmitField, PasswordField, BooleanField)


class BlogPostForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    content = TextAreaField('Content',
                            validators=[DataRequired()])
    submit = SubmitField('Post')


class ContactForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    message = TextAreaField('Message',
                            validators=[DataRequired()])
    submit = SubmitField('Send message')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
