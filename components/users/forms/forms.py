from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, DataRequired, ValidationError
from models.model import User


class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    pass_confirm = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Your username has been registered!")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email has been used!")


class LogInForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class EditProfile(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    submit = SubmitField('Update Profile')

    def validate_username(self, username):
        if username.data == current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError("Your username has been registered!")

    def validate_email(self, email):
        if email.data == current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError("Email has been used!")
