import logging

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from sec_1_api.lib.captcha import captcha_needed
from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.models.device import get_devices_by_user_id

log = logging.getLogger(__name__)


@view_config(context=RootFactory, permission='public', request_method='GET',
             renderer='sec_1_api:templates/index.mako')
def root_view(request):
    if request.user:
        raise HTTPFound(location="home")
    return {"captcha": captcha_needed('login', request)}


@view_config(context=RootFactory, permission='home', request_method='GET',
             renderer='sec_1_api:templates/home.mako', name='home')
def home_view(request):
    devices = get_devices_by_user_id(request.user.id)
    return {
        'devices': devices
    }
