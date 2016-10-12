import asyncio
import logging

from pyramid.view import view_config

from sec_1_api.lib.factories.root import RootFactory
from aiopyramid.websocket.view import WebsocketConnectionView
from aiopyramid.websocket.config import WebsocketMapper
from aiopyramid.websocket.config import UWSGIWebsocketMapper

log = logging.getLogger(__name__)

class ViboWebsocket(WebsocketConnectionView):
    __view_mapper__ = WebsocketMapper


@view_config(name='connect', context=RootFactory)
class Websocket(ViboWebsocket):

    def on_open(self):
        print('connnected')
        yield from self.send('connected')

    def on_message(self, message):
        yield from self.send(message)