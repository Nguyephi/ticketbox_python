from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, DataRequired, ValidationError
from models.model import Event


class CreateEventForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    start_date = DateField('Start Date')
    submit = SubmitField('Create')


class EditEventForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    cover_img = FileField('Update Cover Img')
    description = TextAreaField('Description', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    start_date = DateField('Start Date')
    end_date = DateField('End Date')
    submit = SubmitField('Update Event Info')
