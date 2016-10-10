import logging

from marshamllow import Schema, validate

from sec_1_api.lib.validation import CleanString

log = logging.getLogger(__name__)


class LoginSchema(Schema):
    username = CleanString(required='username is required',
                           validation=validate.length(min=1, max=100))
    password = CleanString(required='password is required',
                           validation=validate.length(min=1, max=100))
