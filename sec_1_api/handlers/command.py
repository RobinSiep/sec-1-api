import asyncio
import glob
import logging
import os

from pyramid.view import view_config
import json

from aiopyramid.websocket.view import WebsocketConnectionView
from aiopyramid.websocket.config import WebsocketMapper
from aiopyramid.websocket.config import UWSGIWebsocketMapper

from marshmallow import ValidationError

from sec_1_api import websockets
from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.lib.security import hash_
from sec_1_api.lib.validation.device import CommandSchema, FirmwareSchema

from sec_1_api.models.firmware import get_latest_firmware
from sec_1_api.models.device import get_device_by_secret_identifier


log = logging.getLogger(__name__)


class ViboWebsocket(WebsocketConnectionView):
    __view_mapper__ = WebsocketMapper


@view_config(name='connect', context=RootFactory)
class Websocket(ViboWebsocket):

    def on_open(self):
        self.identifier = None
        yield from self.send("connected")
        while True:
            # wait for user message
            data = yield from self.ws.recv()
            if data == 'polling for command':
                device = get_device_by_secret_identifier(self.identifier)
                if device:
                    yield from self.send(str(CommandSchema().dump(device).data))
                else:
                    yield from "device not found"
            else:
                try:
                    data = json.loads(data)
                    result, errors = FirmwareSchema(strict=True).load(data)
                    self.identifier = result['identifier']
                    latest_firmware_version = get_latest_firmware(
                    ).firmware_version
                    firmware_version = result['firmwareVersion']
                    if float(firmware_version) < float(latest_firmware_version):
                        # send the firmware
                        root_dir = os.path.dirname(os.path.abspath(__file__))
                        path = '/../firmware/{}'.format(
                            latest_firmware_version)
                        for filename in glob.glob(os.path.join('{}{}'.format(
                                root_dir, path), '*.lua')):
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
                                yield from self.ws.send("RESTORE")
                except (ValueError, KeyError, ValidationError):
                    yield from self.ws.send("No valid json was send")

    def on_message(self, message):
        yield from self.send(message)


@view_config(context=RootFactory,
             name='command',
             permission='public',
             request_method='POST')
def command(request):
    id_ = request.json_body['identifier']
    socket = websockets[id_]
    return {}
