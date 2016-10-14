import asyncio
import glob
import logging
import os

from pyramid.view import view_config
import json

from aiopyramid.websocket.view import WebsocketConnectionView
from aiopyramid.websocket.config import WebsocketMapper
from aiopyramid.websocket.config import UWSGIWebsocketMapper

from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.models.firmware import get_latest_firmware


log = logging.getLogger(__name__)


class ViboWebsocket(WebsocketConnectionView):
    __view_mapper__ = WebsocketMapper


@view_config(name='connect', context=RootFactory)
class Websocket(ViboWebsocket):

    def on_open(self):
        yield from self.send('connected')
        while True:
            # wait for user message
            data = yield from self.ws.recv()
            try:
                data = json.loads(data)
                latest_firmware_version = get_latest_firmware(
                ).firmware_version
                firmware_version = data['firmwareVersion']
                if float(firmware_version) < float(latest_firmware_version):
                    # update the firmware
                    root_dir = os.path.dirname(os.path.abspath(__file__))
                    path = '/../firmware/{}'.format(latest_firmware_version)
                    for filename in glob.glob(os.path.join('{}{}'.format(
                            root_dir, path), '*.lua')):
                        print(filename)
                        yield from self.send('FILE')
                        yield from self.send(filename.split('/')[-1])
                        yield from self.send('____')
                        with open(filename) as f:
                            content = f.readlines()
                            for line in content:
                                yield from self.send(line)
                        result = yield from self.ws.recv()
                        res = json.loads(str(result))
                        if res['result'] == 'true':
                            continue
                        else:
                            break
            except (ValueError, KeyError):
                yield from self.ws.send("No valid json was send")

    def on_message(self, data):
        data = json.loads(data)
