import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.view import view_config

from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.lib.validation.device import LinkDeviceSchema
from sec_1_api.models import commit, persist, rollback
from sec_1_api.models.device import (get_device_by_link_id,
                                     get_devices_by_user_id)

log = logging.getLogger(__name__)


@view_config(permission='device', context=RootFactory, name='device',
             request_method='GET', renderer='sec_1_api:templates/device.mako')
def device_view(request):
    return {"devices": get_devices_by_user_id(request.user.id)}


@view_config(permission='device', context=RootFactory, name='device',
             request_method='PUT', renderer='json')
def link_device(request):
    try:
        result, errors = LinkDeviceSchema(strict=True).load(request.json_body)
    except ValidationError as e:
        raise HTTPBadRequest(json_body=e.messages)

    device = get_device_by_link_id(result['link_id'])

    if result['name']:
        device.name = result['name']
        try:
            persist(device)
        except:
            log.critical("Something went wrong saving the device",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()

    request.user.devices.append(device)

    try:
        persist(request.user)
    except:
        log.critical("Something went wrong saving the user",
                     exc_info=True)
        rollback()
        raise HTTPInternalServerError
    finally:
        commit()
