import logging

from marshmallow import Schema, fields, pre_load, ValidationError

from sec_1_api.lib.validation import CleanString

log = logging.getLogger(__name__)


class PatternSchema(Schema):
    second_0 = CleanString()
    second_1 = CleanString()
    second_2 = CleanString()
    second_3 = CleanString()
    second_4 = CleanString()
    second_5 = CleanString()
    second_6 = CleanString()
    second_7 = CleanString()
    second_8 = CleanString()
    second_9 = CleanString()
    second_10 = CleanString()
    second_11 = CleanString()

    @pre_load
    def validate_data(self, data):
        for field in data:
            if data[field] != "1":
                raise ValidationError({data[field]: "invalid input"})
