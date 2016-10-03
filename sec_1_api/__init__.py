import logging

from pyramid.config import Configurator
from pyramid.renderers import JSON
from sqlalchemy import engine_from_config

from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.models.meta import DBSession, Base

log = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings,
                          root_factory=RootFactory)

    config.add_renderer(None, JSON())
    config.scan('sec_1_api.handlers')

    return config.make_wsgi_app()
