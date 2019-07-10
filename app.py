import os
from flask import Flask, render_template, redirect, url_for, request, flash
from components.users import users_blueprint
from components.events import events_blueprint
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_user, login_required, logout_user, LoginManager, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models.model import db, User, RatingUser, TicketType
from components.events.forms.forms import Event, UploadPhoto


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/static/cover_img'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db.init_app(app)
migrate = Migrate(app, db, compare_type=True)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


POSTGRES = {
    'user': os.environ['POSTGRES_USER'],
    'pw': os.environ['POSTGRES_PWD'],
    'db': os.environ['POSTGRES_DB'],
    'host': os.environ['POSTGRES_HOST'],
    'port': os.environ['POSTGRES_PORT'],
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:\
%(port)s/%(db)s' % POSTGRES

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/', methods=['GET', 'POST'])
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)


app.register_blueprint(users_blueprint, url_prefix='/users')

app.register_blueprint(events_blueprint, url_prefix='/events')


if __name__ == '__main__':
    app.run(debug=True)
