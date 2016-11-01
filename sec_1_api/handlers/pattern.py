import logging

from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.view import view_config
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.lib.validation.pattern import PatternSchema

from sec_1_api.models import commit, persist, rollback
from sec_1_api.models.device import get_device_by_link_id


log = logging.getLogger(__name__)


@view_config(context=RootFactory,
             name='pattern',
             permission='public',
             request_method='POST',
             renderer='json')
def post_pattern(request):

    try:
        result, errors = PatternSchema(strict=True).load(request.json_body)
    except ValidationError as e:
        raise HTTPBadRequest(json_body=e.messages)

    try:
        device = get_device_by_link_id(result['device_link_id'],
                                       request.user.id)
    except NoResultFound:
        raise HTTPBadRequest(json={"device": "not found"})
    except KeyError:
        raise HTTPBadRequest(json={"device_link_id": "no device selected"})

    vibrate_pattern = []
    pattern_length = 11
    for i in range(pattern_length):
        try:
            vibrate_pattern.append(int(result['second_{}'.format(i)]))
        except KeyError:
            vibrate_pattern.append(0)

    device.pattern = str(vibrate_pattern)

    try:
        if result['on']:
            device.on = True
    except KeyError:
        device.on = False

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

    return {}
