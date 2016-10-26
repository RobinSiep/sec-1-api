import logging

from pyramid.view import view_config

from sec_1_api.lib.factories.root import RootFactory

log = logging.getLogger(__name__)


@view_config(permission='device', context=RootFactory, name='device',
             request_method='GET', renderer='sec_1_api:templates/device.mako')
def device_view(request):
    return {}


@view_config(permission='device', context=RootFactory, name='device',
             request_method='POST', renderer='json')
def add_device(request):
    return {}
