from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, DataRequired, ValidationError
from models.model import Event
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

photos = UploadSet('photos', IMAGES)


class CreateEventForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    start_date = DateField('Start Date')
    submit = SubmitField('Create')


class AddTicketType(FlaskForm):
    ticket_type = StringField('Ticket Type', validators=[InputRequired()])
    ticket_price = IntegerField('Ticket Type', validators=[InputRequired()])
    quantity = IntegerField('Quantity', validators=[InputRequired()])
    submit = SubmitField('Add Tickets')


class BuyTicket(FlaskForm):
    ticket_type = SelectField('Select Ticket Type', coerce=int)
    quantity = IntegerField('Quantity', validators=[InputRequired()])
    submit = SubmitField('Buy Tickets')


class EditEventForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    start_date = DateField('Start Date')
    end_date = DateField('End Date')
    submit = SubmitField('Update Event Info')


class UploadPhoto(FlaskForm):
    cover_img = FileField(validators=[FileAllowed(
        photos, u'Image only!'), FileRequired(u'File was empty!')])
    submit = SubmitField(u'Upload')
