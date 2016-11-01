import logging

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config
from marshmallow import ValidationError

from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.lib.validation.command import PatternSchema


log = logging.getLogger(__name__)


@view_config(context=RootFactory,
             name='command',
             permission='public',
             request_method='POST',
             renderer='sec_1_api:templates/home.mako')
def command(request):

    try:
        result, errors = PatternSchema(strict=True).load(request.json_body)
    except ValidationError as e:
        raise HTTPBadRequest(json_body=e.messages)

    pattern = {}
    pattern_length = 12
    for i in range(pattern_length):
        try:
            pattern[i] = int(result[i])
        except KeyError:
            pattern[i] = 0
    log.info(pattern)
    return {}
