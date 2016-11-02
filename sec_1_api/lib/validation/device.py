import logging

from marshmallow import Schema, validate, post_load,  ValidationError
from sqlalchemy.orm.exc import NoResultFound

from sec_1_api.lib.validation import CleanString
from sec_1_api.models.device import get_device_by_link_id

log = logging.getLogger(__name__)


class LinkDeviceSchema(Schema):
    link_id = CleanString(required='link_id is required',
                          validation=validate.Length(equal=24))
    name = CleanString(validation=validate.Length(max=250))

    @post_load
    def validate_device_exists(self, data):
        try:
            get_device_by_link_id(data['link_id'])
        except NoResultFound:
            raise ValidationError({
                "link_id": "No device was found for the given link_id"
            })


def validate_name_unique(user, name):
    device = user.devices.filter_by(name=name).one_or_none()

    if device:
        return

    raise ValidationError({
        "name": "You already have a device with this name!"
    })


class UnlinkDeviceSchema(Schema):
    name = CleanString(required=True, validation=validate.Length(max=250))


class FirmwareSchema(Schema):
    identifier = CleanString(required='identifier is required')
    firmware_version = CleanString(
        required='firmware version is required', load_from='firmwareVersion')
