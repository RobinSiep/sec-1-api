import asyncio
import glob
import logging
import os
import time

from pyramid.view import view_config
import json

from aiopyramid.websocket.view import WebsocketConnectionView
from aiopyramid.websocket.config import WebsocketMapper
from aiopyramid.websocket.config import UWSGIWebsocketMapper

from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from sec_1_api import websockets
from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.lib.security import hash_
from sec_1_api.lib.validation.device import CommandSchema, FirmwareSchema

from sec_1_api.models.firmware import get_latest_firmware
from sec_1_api.models.device import get_device_by_secret_identifier


log = logging.getLogger(__name__)


@view_config(name='connect', context=RootFactory, mapper=WebsocketMapper)
class Websocket(WebsocketConnectionView):

    def on_open(self):
        self.identifier = None
        self.change = False
        yield from self.send("connected")
        while True:
            # wait for user message
            time.sleep(2)
            log.info(self.identifier)
            if self.identifier:
                log.info(self.identifier)
                change = False
                try:
                    device = get_device_by_secret_identifier(self.identifier)
                    yield from self.send(str(CommandSchema.dump(device).data))
                except NoResultFound:
                    yield from self.send(str({'message': 'device not found'}))

    def on_message(self, message):
        yield from self.send(message)
        try:
            data = json.loads(message)
            result, errors = FirmwareSchema(strict=True).load(data)
            self.identifier = result['identifier']
            latest_firmware_version = get_latest_firmware(
            ).firmware_version
            global websockets
            websockets[self.identifier] = self
            log.info(websockets)
            firmware_version = result['firmware_version']
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
        except ValidationError as e:
            yield from self.ws.send(str({'message': str(e)}))


@view_config(context=RootFactory,
             name='command',
             permission='public',
             request_method='POST')
def command(request):
    id_ = request.json_body['identifier']
    socket = websockets[id_]
    socket.change = True
    log.info(websockets)
    log.info(socket)
    return
