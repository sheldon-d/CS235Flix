from flask import Blueprint, render_template, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator
from functools import wraps

import movie_app.blueprints.utilities as utilities
import movie_app.services.auth_services as services
import movie_app.adapters.repository as repo

# Configure Blueprint.
authentication_blueprint = Blueprint('authentication_bp', __name__, url_prefix='/authentication')


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message='Your username is required'),
        Length(min=3, message='Your username is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Login')


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_not_unique = None

    if form.validate_on_submit():
        # Successful POST results if the username and password have passed validation checking.
        # Using the service layer to attempt to add the new user.
        try:
            services.add_user(form.username.data, form.password.data, repo.repo_instance)

            # If there are no issues, the user is redirected to the login page.
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            username_not_unique = 'Sorry that username is already taken. Please enter another.'

    # For a GET or a failed POST request, return the Registration Web page.
    return render_template(
        'authentication/credentials.html',
        title='Register',
        form=form,
        username_error_message=username_not_unique,
        handler_url=url_for('authentication_bp.register'),
        random_movies=utilities.get_random_movies()
    )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_not_recognised = None
    password_does_not_match_username = None

    if form.validate_on_submit():
        # Successful POST results if the username and password have passed validation checking.
        # Using the service layer to lookup the user.
        try:
            user = services.get_user(form.username.data, repo.repo_instance)

            # Authenticate user.
            services.authenticate_user(user.user_name, form.password.data, repo.repo_instance)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['username'] = user.user_name
            return redirect(url_for('home_bp.home'))

        except services.UnknownUserException:
            # Username not known to the system, set a suitable error message.
            username_not_recognised = 'Sorry that username not recognised. Please enter another.'

        except services.AuthenticationException:
            # Authentication failed, set a suitable error message.
            password_does_not_match_username = 'Sorry that password does not match the supplied username. ' \
                                               'Please check and try again.'

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'authentication/credentials.html',
        title='Login',
        username_error_message=username_not_recognised,
        password_error_message=password_does_not_match_username,
        form=form,
        selected_articles=utilities.get_random_movies()
    )


@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view
