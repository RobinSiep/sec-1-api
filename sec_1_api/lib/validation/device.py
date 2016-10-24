import logging

from marshmallow import Schema
from marshmallow.fields import Boolean

from sec_1_api.lib.validation import CleanString

log = logging.getLogger(__name__)


class CommandSchema(Schema):
    pattern = CleanString(dump_only=True)
    on = Boolean(dump_only=True)


class FirmwareSchema(Schema):
    identifier = CleanString(required='identifier is required')
    firmware_version = CleanString(
        required='firmware version is required', load_from='firmwareVersion')
