import logging

from pyramid.view import view_config

from sec_1_api.lib.factories.root import RootFactory

log = logging.getLogger(__name__)


@view_config(context=RootFactory, permission='firmware', name='firmware',
             renderer="sec_1_api:templates/firmware.mako",
             request_method='GET')
def firmware_view(request):
    return {}
