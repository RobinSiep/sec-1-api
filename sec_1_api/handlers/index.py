import logging

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from sec_1_api.lib.factories.root import RootFactory

log = logging.getLogger(__name__)


@view_config(context=RootFactory, permission='public', request_method='GET',
             renderer='sec_1_api:templates/index.mako')
def root_view(request):
    if request.user:
            raise HTTPFound(location="home")
    return {}


@view_config(context=RootFactory, permission='public', request_method='GET',
             renderer='sec_1_api:templates/home.mako', name='home')
def home_view(request):
    return {}
