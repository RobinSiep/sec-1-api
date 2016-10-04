import logging

from pyramid.view import view_config

from sec_1_api.lib.encryption import encrypt
from sec_1_api.lib.factories.root import RootFactory


log = logging.getLogger(__name__)


@view_config(context=RootFactory, permission='public', renderer='json',
             request_method='GET')
def root_view(request):
    return {"sec-1-api": "0.1"}


@view_config(context=RootFactory, permission='public', renderer='json',
             request_method='GET', name='command')
def command(request):

    try:
        identifier = request.headers['identifier']
    except KeyError:
        return {"error": "identifier not found"}

    command = encrypt(identifier, "vibrate")
    return {"command": command}
