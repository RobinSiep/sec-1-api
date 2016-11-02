import glob
import json
import logging
import os
import signal
import sys

from marshmallow import ValidationError

from sec_1_api.lib.validation.device import FirmwareSchema
from sec_1_api.models.firmware import get_latest_firmware
from sec_1_api.websocket.SimpleWebSocketServer import (WebSocket,
                                                       SimpleWebSocketServer)

log = logging.getLogger(__name__)

file_template = "FILE\n{filename}\n_____\n{content}"


class SimpleEcho(WebSocket):
    def __init__(self, *args, **kwargs):
        super().__init_(*args, **kwargs)
        self.identifier = None
        self.files = None
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        latest_firmware_version = get_latest_firmware()
        self.path = '/../sec_1_api/firmware/{}'.format(
                latest_firmware_version)

    def handleMessage(self):
        log.info("handling message")
        data = json.loads(self.data)
        if data['result'] is False:
            self.sendMessage("RESTORE")
        elif data['result'] is None:
            try:
                result, errors = FirmwareSchema(strict=True).load(data)
            except ValidationError as e:
                self.sendMessage(str({"message": str(e)}))
            self.identifier = result['identifier']

            firmware_version = result['firmware_version']
            latest_firmware_version = get_latest_firmware()
            if float(firmware_version) < float(latest_firmware_version):
                self.path = '/../sec_1_api/firmware/{}'.format(
                   latest_firmware_version)
                self.files = [filename for filename in glob.glob(
                    os.path.join('{}{}'.format(self.root_dir, self.path),
                                 '*.lua')
                )]

        # send the firmware
        if not self.files:
            self.sendMessage("UPDATE FINISH")
        filename = self.files[0]
        del self.files[0]

        with open(filename) as f:
            content = f.readlines()
        file_data = file_template.format(filename=filename.split('/')[-1],
                                         content=content)
        self.sendMessage(str(file_data))

    def handleConnected(self):
        log.info("connected")
        pass

    def handleClose(self):
        pass


def serve(settings):
    cls = SimpleEcho

    # server = SimpleSSLWebSocketServer(options.host, options.port, cls,
    #                                   options.cert, options.cert,
    #                                   version=options.ver)
    server = SimpleWebSocketServer(settings['websocket.host'],
                                   int(settings['websocket.port']), cls)

    def close_sig_handler(signal, frame):
        server.close()
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)
    log.info("booting up websocket server")

    server.serveforever()
