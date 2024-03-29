from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, LoginManager, UserMixin, current_user
from components.users.forms.forms import SignUpForm, LogInForm, EditProfile
from models.model import User, db, Event
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed


users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(name=form.name.data, username=form.username.data,
                        email=form.email.data)
        new_user.set_password(form.password.data)
        flash(
            f'Hey {form.username.data.capitalize()}, you have successfully created a new account! Please login to create and buy events.', 'success')
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        # preprocess username
        username = form.username.data.strip()
        log_user = User.query.filter_by(username=username).first()
        if log_user is None:
            # flash('Invalid Username')
            form.username.errors.append("Invalid Username")
            return render_template('login.html', form=form, signup_modal_form=SignUpForm())

        if not log_user.check_password(form.password.data):
            form.password.errors.append("Invalid password")
            return render_template('login.html', form=form, signup_modal_form=SignUpForm())

        login_user(log_user)
        return render_template('welcome.html')

    return render_template('login.html', form=form, signup_modal_form=SignUpForm())


@users_blueprint.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')


@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@users_blueprint.route('/editprofile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfile()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data.lower()
        current_user.email = form.email.data
        flash(f'Your account has been updated!', 'success')
        db.session.commit()
    return render_template('profile.html', form=form)


@users_blueprint.route('/<int:user_id>/delete')
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user.id == current_user.id:
        flash('Account deleted!', 'success')
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))


@users_blueprint.route('/eventscreated')
@login_required
def users_events():
    user = current_user
    events = user.creator_id
    return render_template('users_events.html', events=events, user=user)
