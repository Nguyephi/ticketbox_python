import os
import secrets

from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user, LoginManager, UserMixin, current_user
from flask_wtf.file import FileField, FileAllowed
from models.model import db, Event, User
from components.events.forms.forms import CreateEventForm, EditEventForm


events_blueprint = Blueprint('events', __name__, template_folder='templates')


@events_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def createevent():
    form = CreateEventForm()
    if form.validate_on_submit():

        new_event = Event(title=form.title.data, creator_id=current_user.id,
                          description=form.description.data, location=form.location.data, start_date=form.start_date.data
                          )

        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('create_event.html', form=form)


@events_blueprint.route('/<int:event_id>', methods=['GET', 'POST'])
def eventcard(event_id):

    eventcard = Event.query.filter_by(id=event_id).one()
    creator_id = eventcard.creator_id
    location = eventcard.location
    start_date = eventcard.start_date
    end_date = eventcard.end_date

    return render_template('eventpage.html', eventcard=eventcard)


@events_blueprint.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.filter_by(id=event_id).one()
    form = EditEventForm()
    if form.validate_on_submit():

        event.title = form.title.data
        event.description = form.description.data
        event.location = form.location.data
        event.start_date = form.start_date.data
        event.end_date = form.end_date.data
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('editevent.html', form=form, event=event)


@events_blueprint.route('/<int:event_id>/delete')
@login_required
def delete_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event.creator_id == current_user.id:
        flash('Event deleted!')
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('index'))
