import logging

from marshmallow import Schema

from sec_1_api.lib.validation import CleanString

log = logging.getLogger(__name__)


class LinkDeviceSchema(Schema):
    link_id = CleanString(required='link_id is required')
    name = CleanString()
