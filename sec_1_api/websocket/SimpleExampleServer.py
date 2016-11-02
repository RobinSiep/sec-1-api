import glob
import json
import logging
import os
import signal
import sys
from multiprocessing import Pool

from marshmallow import ValidationError

from sec_1_api.lib.validation.device import FirmwareSchema
from sec_1_api.models.firmware import get_latest_firmware
from sec_1_api.models.device import get_device_by_secret_identifier
from sec_1_api.websocket.SimpleWebSocketServer import (WebSocket,
                                                       SimpleWebSocketServer)

log = logging.getLogger(__name__)

file_template = "FILE\n{filename}\n_____\n{content}"


class SimpleEcho(WebSocket):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.identifier = None
        self.files = None
        self.pool = None
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        log.info("woop")
        self.path = "/../sec_1_api/firmware/1.0.2"
        log.info("boop")


    def handleMessage(self):
        log.info("handling message")
        data = json.loads(self.data)
        log.info(data)
        if data.get('identifier'):
            log.info("identifying")
            self.pool = Pool(processes=1)
            self.pool.apply_async(self.poll_for_command, [data['identifier']])
        if data.get('result') is False:
            log.info("restoring")
            self.sendMessage("RESTORE")
        elif data.get('result') is None:
            log.info("checking firmware")
            try:
                result, errors = FirmwareSchema(strict=True).load(data)
            except ValidationError as e:
                log.info("validation error")
                self.sendMessage(str({"message": str(e)}))
            self.identifier = result['identifier']

            firmware_version = result['firmware_version']
            # latest_firmware_version = get_latest_firmware().firmware_version
            log.info("comparins versions")
            # if float(firmware_version) < float(latest_firmware_version):
            log.info("updating versions")
            self.path = '/../sec_1_api/firmware/1.0.2'
            self.files = [filename for filename in glob.glob(
                os.path.join('{}{}'.format(self.root_dir, self.path),
                             '*.lua')
            )]

        log.info("updating")
        # send the firmware
        if not self.files:
            log.info("update finish")
            self.sendMessage("UPDATE FINISH")
        filename = self.files[0]
        del self.files[0]

        with open(filename) as f:
            content = f.readlines()
        file_data = file_template.format(filename=filename.split('/')[-1],
                                         content=content)
        log.info("sending file")
        self.sendMessage(str(file_data))

    def handleConnected(self):
        log.info("connected")
        pass

    def handleClose(self):
        if self.pool:
            self.pool.terminate()
        log.info("closed")


    def poll_for_command(self, identifier):
        log.info("called")
        time.sleep(500)
        try:
            device = get_device_by_secret_identifier(identifier)
            self.sendMessage(str(CommandSchema.dump(device).data))
        except NoResultFound:
            self.sendMessage(str({'message': 'device not found'})) 


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
    log.info("booting up websocket server {}:{}".format(settings['websocket.host'],
                                                        settings['websocket.port']))

    server.serveforever()
