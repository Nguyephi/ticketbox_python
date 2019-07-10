import os
import secrets

from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user, LoginManager, UserMixin, current_user
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, IMAGES
from models.model import db, Event, User, LikeEvent, TicketType
from components.events.forms.forms import CreateEventForm, EditEventForm, UploadPhoto, AddTicketType, BuyTicket
from models.model import Orders


events_blueprint = Blueprint('events', __name__, template_folder='templates')

photos = UploadSet('photos', IMAGES)


@events_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def createevent():
    form = CreateEventForm()
    if form.validate_on_submit():
        new_event = Event(title=form.title.data, creator_id=current_user.id,
                          description=form.description.data, location=form.location.data, start_date=form.start_date.data
                          )
        flash(
            f'You have successfully created a new event', 'success')
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('create_event.html', form=form)


@events_blueprint.route('<int:event_id>/addtickettype', methods=['GET', 'POST'])
@login_required
def add_ticket_type(event_id):
    form = AddTicketType()
    event = Event.query.filter_by(id=event_id).one()
    if form.validate_on_submit():
        add_ticket = TicketType(ticket_type=form.ticket_type.data,
                                ticket_price=form.ticket_price.data, quantity=form.quantity.data)
        event.ticket_type.append(add_ticket)
        flash(
            f'You added {form.ticket_type.data} ticket to the {event.title.capitalize()} event!', 'success')
        db.session.add(add_ticket)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_ticket_type.html', form=form)


@events_blueprint.route('/<int:event_id>', methods=['GET', 'POST'])
def eventcard(event_id):
    eventcard = Event.query.filter_by(id=event_id).one()
    user = User.query.filter_by(id=eventcard.creator_id).one()
    tickets = TicketType.query.filter_by(event_id=eventcard.id).all()

    return render_template('eventpage.html', eventcard=eventcard, user=user, tickets=tickets)


@events_blueprint.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.filter_by(id=event_id).one()
    form = EditEventForm()
    photo_form = UploadPhoto()
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.location = form.location.data
        event.start_date = form.start_date.data
        event.end_date = form.end_date.data
        db.session.commit()
        flash(
            f'Your event has been updated', 'success')
        return redirect(url_for('index'))

    return render_template('editevent.html', form=form, event=event, photo_form=photo_form)


@events_blueprint.route('/<int:event_id>/upload_image', methods=['GET', 'POST'])
def upload_image(event_id):
    photo_form = UploadPhoto()
    event = Event.query.filter_by(id=event_id).one()
    if photo_form.validate_on_submit():
        filename = photos.save(photo_form.cover_img.data)
        file_url = photos.url(filename)
        flash(f'Your image has been uploaded to your event', 'success')
        event.cover_img = filename
        db.session.commit()
    else:
        file_url = None
        flash(f'File not accepted', 'danger')
    return redirect(url_for('index'))


@events_blueprint.route('/<int:event_id>/delete')
@login_required
def delete_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event.creator_id == current_user.id:
        flash('Event deleted!', 'success')
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('index'))


@events_blueprint.route('/<event_id>/buyticket', methods=['POST', 'GET'])
@login_required
def buy_ticket(event_id):
    event = Event.query.filter_by(id=event_id).one()
    tickets = event.ticket_type
    form = BuyTicket()
    ticket_types = [(ticket.id, ticket.ticket_type + " - Voucher price: $" + str(
        ticket.ticket_price) + " - Quantity left: " + str(ticket.quantity)) for ticket in tickets]
    form.ticket_type.choices = ticket_types
    if form.validate_on_submit():
        ticket = TicketType.query.filter_by(id=form.ticket_type.data).first()
        total_amount = form.quantity.data * ticket.ticket_price
        purchase = Orders(quantity=form.quantity.data,
                          buyer_id=current_user.id,
                          event_id=event_id,
                          tickettype_id=form.ticket_type.data,
                          total_bill=total_amount)
        db.session.add(purchase)
        db.session.commit()
        flash(f'Purchase successful!', 'success')
        return redirect(url_for('index'))
    return render_template('buy_ticket.html', event=event, tickets=tickets, form=form)


@events_blueprint.route('likeevent/<int:event_id>')
@login_required
def like_event(event_id):
    like = LikeEvent.query.filter_by(
        event_id=event_id, user_id=current_user.id).first()
    event = Event.query.get(event_id)
    if event.like_count == None:
        event.like_count += 1
        is_liked = LikeEvent(user_id=current_user.id,
                             event_id=event.id, like=1)
        db.session.add(is_liked)
        db.session.commit()
    return redirect(url_for('index'))
