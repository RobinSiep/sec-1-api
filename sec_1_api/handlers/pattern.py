import asyncio
import glob
import json
import logging
import os
import time

from pyramid.httpexceptions import (HTTPOk, HTTPBadRequest,
                                    HTTPInternalServerError)
from pyramid.view import view_config

from aiopyramid.websocket.view import WebsocketConnectionView
from aiopyramid.websocket.config import WebsocketMapper
from aiopyramid.websocket.config import UWSGIWebsocketMapper

from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.lib.validation.pattern import PatternSchema

from sec_1_api.models import commit, persist, rollback
from sec_1_api.models.firmware import get_latest_firmware
from sec_1_api.models.device import (get_device_by_link_id,
                                     get_devices_by_user_id)


log = logging.getLogger(__name__)


@view_config(context=RootFactory,
             name='pattern',
             permission='public',
             request_method='GET',
             renderer='JSON')
def pattern(request):
    return {}


@view_config(context=RootFactory,
             name='pattern',
             permission='public',
             request_method='POST',
             renderer='json')
def pattern(request):

    try:
        result, errors = PatternSchema(strict=True).load(request.json_body)
    except ValidationError as e:
        raise HTTPBadRequest(json_body=e.messages)

    try:
        device = get_device_by_link_id(result['device_link_id'])
    except NoResultFound:
        raise HTTPBadRequest(json={"device": "not found"})

    pattern = {}
    pattern_length = 12
    for i in range(pattern_length):
        try:
            pattern[i] = int(result[i])
        except KeyError:
            pattern[i] = 0

    device.pattern = pattern
    try:
        persist(device)
    except:
        log.critical(
            'Something went wrong saving the {}'.format(
                device.__class__.__name__),
            exc_info=True)
        rollback()
        raise HTTPInternalServerError
    finally:
        commit()

    return {

    }
