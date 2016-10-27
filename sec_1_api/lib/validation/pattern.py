import logging

from marshmallow import Schema, fields, pre_load, ValidationError

from sec_1_api.lib.validation import CleanString

log = logging.getLogger(__name__)


def validate_data(data):
    if data != "1":
        raise ValidationError({data[field]: "invalid input"})


class PatternSchema(Schema):
    device_link_id = CleanString()
    second_0 = CleanString(validate=validate_data)
    second_1 = CleanString(validate=validate_data)
    second_2 = CleanString(validate=validate_data)
    second_3 = CleanString(validate=validate_data)
    second_4 = CleanString(validate=validate_data)
    second_5 = CleanString(validate=validate_data)
    second_6 = CleanString(validate=validate_data)
    second_7 = CleanString(validate=validate_data)
    second_8 = CleanString(validate=validate_data)
    second_9 = CleanString(validate=validate_data)
    second_10 = CleanString(validate=validate_data)
    second_11 = CleanString(validate=validate_data)
