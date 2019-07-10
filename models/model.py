from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# from components.users.forms.forms import SignUpForm

db = SQLAlchemy()


class RatingUser(db.Model):
    __tablename__ = 'rating_users'
    id = db.Column(db.Integer, primary_key=True)
    rater_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    target_user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)


class LikeEvent(db.Model):
    __tablename__ = 'like_event'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    isLiked = db.Column(db.Integer, default=0)


class TicketType(db.Model):
    __tablename__ = 'ticket_types'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    ticket_type = db.Column(db.String(15))
    ticket_price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    order = db.relationship('Orders', backref='ticket_types')


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    tickettype_id = db.Column(db.Integer, db.ForeignKey('ticket_types.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    quantity = db.Column(db.Integer, default=0)
    total_bill = db.Column(db.Integer, nullable=False)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'))
    title = db.Column(db.String(255), nullable=False)
    cover_img = db.Column(db.String(500), default=('download.jpeg'))
    description = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    like_count = db.Column(db.Integer, nullable=False, default=0)

    likes = db.relationship('LikeEvent', backref='events')
    ticket_type = db.relationship('TicketType', backref='events')
    event = db.relationship('Orders', backref='events')


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    rater_id = db.relationship(
        'RatingUser', primaryjoin=(id == RatingUser.rater_id))
    target_user_id = db.relationship(
        'RatingUser', primaryjoin=(id == RatingUser.target_user_id))

    creator_id = db.relationship(
        'Event', primaryjoin=(id == Event.creator_id))

    likes = db.relationship('LikeEvent', backref='users')
    buyer = db.relationship('Orders', backref='users')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
