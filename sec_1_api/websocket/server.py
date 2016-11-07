import asyncio
import threading
import glob
import json
import logging
import os
import signal
import sys
import time
from concurrent.futures import ProcessPoolExecutor as Pool

from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from sec_1_api.lib.validation.device import CommandSchema, FirmwareSchema
from sec_1_api.models import expunge
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
        self.poll = False
        self.pattern = None
        self.on = None
        self.stop = False
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.path = "/../sec_1_api/firmware/1.0.2"
        thread = threading.Thread(target=self.poll_loop)
        thread.start() 
        log.info("init")

    def poll_loop(self):
        if self.stop:
            return
        log.info("poll")
        log.info(self.poll)
        if self.poll:
             self.poll_for_command(self.identifier)
        time.sleep(5)
        self.poll_loop()

    def handleMessage(self):
        try:
            log.info("handling message")
            data = json.loads(self.data)
            log.info(data)
            if data.get('identifier'):
                log.info("identifying")
                self.identifier = data['identifier']
                self.poll = True
                return
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

            latest_firmware_version = get_latest_firmware().firmware_version
            log.info("comparing versions")
            if float(firmware_version) < float(latest_firmware_version):
                log.info("updating versions")
                self.path = '/../sec_1_api/firmware/1.0.2'
                self.files = [filename for filename in glob.glob(
                os.path.join('{}{}'.format(self.root_dir, self.path),
                             '*.lua')
                )]

                log.info("updating")

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
        except Exception as e:
            log.info(str(e))

    def handleConnected(self):
        log.info("connected")
        pass

    def handleClose(self):
        self.stop = True
        log.info("closed")


    def poll_for_command(self, identifier):
        log.info("polling for command")
        try:
            device = get_device_by_secret_identifier(identifier)
            if device.on != self.on or device.pattern != self.pattern:
                self.pattern = device.pattern
                self.on = device.on
                self.sendMessage(str(CommandSchema().dump(device).data))
                log.info("send {}".format(str(CommandSchema().dump(device).data)))
            else:
                log.info("no change")
            expunge(device)
        except NoResultFound:
            log.info("no device found")
            self.sendMessage(str({'message': 'device not found'})) 

def serve(settings):
    log.info("init websocket")
    try:
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
    except Exception as e:
        log.info(str(e))
