import logging

from pyramid.view import view_config

from sec_1_api.lib.factories.root import RootFactory

log = logging.getLogger(__name__)


@view_config(context=RootFactory, permission='public', renderer='json',
             request_method="POST", name="login")
def login(request):
    return {}
