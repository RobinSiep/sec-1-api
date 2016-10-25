import logging

from marshmallow import Schema, post_load, validate,  ValidationError

from sec_1_api.lib.validation import CleanString
from sec_1_api.lib.validation.auth import validate_password

log = logging.getLogger(__name__)


class SendRecoverSchema(Schema):
    email = CleanString(required='email is required')

    @post_load
    def verify_email(self, data):
        _verify_email(data)


class RecoverSchema(Schema):
    email = CleanString(required='email is required')
    password = CleanString(required='password is required',
                           validation=validate.Length(min=1, max=100))
    password_confirm = CleanString(required='password_confirm is required')
    recovery_code = CleanString(required='recovery code is required',
                                validation=validate.Length(equal=8))

    @post_load
    def verify_email(self, data):
        _verify_email(data)

    @post_load
    def compare_passwords(self, data):
        if data['password'] != data['password_confirm']:
            raise ValidationError({"password": "Passwords do not match"})

    @post_load
    def validate_password(self, data):
        validate_password(data)


def _verify_email(data):
    email = data['email']

    if '@' and '.' not in email:
        raise ValidationError({"email": "Invalid email"})
