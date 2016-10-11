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

from socketio.server import SocketIOServer
from pyramid.paster import get_app
from gevent import monkey; monkey.patch_all()

if __name__ == '__main__':

    app = get_app('rik.ini')
    print 'Listening on port http://0.0.0.0:8080 and on port 10843 (flash policy server)'

    SocketIOServer(('0.0.0.0', 8080), app,
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 10843)).serve_forever()