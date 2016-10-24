import logging
import re

from marshmallow import Schema, validate, post_load, ValidationError
from sqlalchemy.orm.exc import NoResultFound

from sec_1_api.lib.validation import CleanString
from sec_1_api.models.user import get_user_by_username

log = logging.getLogger(__name__)


class LoginSchema(Schema):
    username = CleanString(required='username is required',
                           validation=validate.Length(min=1, max=100))
    password = CleanString(required='password is required',
                           validation=validate.Length(min=1, max=100))


class RegisterSchema(Schema):
    username = CleanString(required='username is required',
                           validation=validate.Length(min=1, max=100))
    email = CleanString()
    password = CleanString(required='password is required',
                           validation=validate.Length(min=1, max=100))
    password_confirm = CleanString(required='password_confirm is required')

    @post_load
    def compare_passwords(self, data):
        if data['password'] != data['password_confirm']:
            raise ValidationError({"password": "Passwords do not match"})

    @post_load
    def validate_password(self, data):
        validate_password(data)

    @post_load
    def check_existing_username(self, data):
        try:
            get_user_by_username(data['username'])
        except NoResultFound:
            # If there's not user found we can safely continue
            return
        raise ValidationError({
            "username": "a user with this username already exists!"})

    @post_load
    def verify_email(self, data):
        email = data['email']

        if not email:
            return

        if '@' and '.' not in email:
            raise ValidationError('Invalid email')


def has_spaces(password):
    return ' ' in password


def has_letters(password):
    return bool(re.search('[a-zA-Z]', password))


def has_numbers(password):
    _digits = re.compile('\d')
    return bool(_digits.search(password))


def validate_password(data):
    password = data['password']
    error = {"password": ""}

    if has_spaces(password):
        error['password'] = 'Password may not contain any spaces'
    elif not has_numbers(password):
        error['password'] = 'Password must contain at least 1 number'
    elif not has_letters(password):
        error['password'] = 'Password must contain at least 1 letter'
    else:
        return
    raise ValidationError(error)
