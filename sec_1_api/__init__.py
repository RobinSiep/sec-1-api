import logging

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.renderers import JSON
from pyramid.security import authenticated_userid
from sqlalchemy import engine_from_config

from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.models.meta import DBSession, Base
from sec_1_api.models.user import get_user_by_id
from sec_1_api.handlers.command import command

from gevent import monkey
monkey.patch_all()

log = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authentication_policy = AuthTktAuthenticationPolicy(
        secret=settings['auth.secret'],
        timeout=settings.get('auth.timeout'),
        reissue_time=settings.get('auth.reissue_time'),
        http_only=True,
        hashalg='sha512')



    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=ACLAuthorizationPolicy(),
                          root_factory=RootFactory)
    config.set_request_property(get_user, 'user', reify=True)
    config.add_route('command', '/command')
    config.add_view(command, route_name='command', renderer='json')
    config.add_renderer(None, JSON())
    config.scan('sec_1_api.handlers')

    return config.make_wsgi_app()


def get_user(request):
    user_id = authenticated_userid(request)
    if user_id is not None:
        return get_user_by_id(user_id)
    return None
