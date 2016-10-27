import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.view import view_config
from sqlalchemy.orm.exc import NoResultFound

from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.lib.validation.device import (LinkDeviceSchema,
                                             UnlinkDeviceSchema)
from sec_1_api.models import commit, persist, rollback
from sec_1_api.models.device import (Device, get_device_by_link_id,
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


@view_config(permission='device', context=RootFactory, name='device',
             requrest_method='DELETE', renderer='json')
def unlink_device(request):
    try:
        result, errors = UnlinkDeviceSchema(strict=True).load(
            request.json_body)
    except ValidationError as e:
        raise HTTPBadRequest(json_body=e.messages)

    user = request.user
    try:
        device = user.devices.filter(Device.name == result['name']).one()
    except NoResultFound:
        raise HTTPBadRequest(json_body={
            'name': 'No device found for given name'
        })

    user.device.remove(device)

    try:
        persist(user)
    except:
        log.critical("Something went wrong unlinking the device",
                     exc_info=True)
        rollback()
        raise HTTPInternalServerError
    finally:
        commit()
