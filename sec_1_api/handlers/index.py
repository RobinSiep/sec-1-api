import logging

from pyramid.view import view_config

from sec_1_api.lib.factories.root import RootFactory

log = logging.getLogger(__name__)


@view_config(context=RootFactory, permission='public', request_method='GET',
             renderer='sec_1_api:templates/index.mako')
def root_view(request):
    return {}

@view_config(context=RootFactory, permission='public', request_method='GET',
			 renderer='sec_1_api:templates/home.mako', name='home')
def home_view(request):
	return {}
