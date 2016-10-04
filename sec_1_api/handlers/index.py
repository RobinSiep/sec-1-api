import logging

from pyramid.view import view_config
from sec_1_api.lib.encryption import encrypt_aes_base64
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

    command = encrypt_aes_base64(
        "vibrate", request.registry.settings['sync_encryption_key'])

    return {"do": command}
