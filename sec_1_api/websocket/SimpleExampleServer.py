import logging
import signal
import sys
from sec_1_api.websocket.SimpleWebSocketServer import (WebSocket,
                                                       SimpleWebSocketServer)

log = logging.getLogger(__name__)


class SimpleEcho(WebSocket):

    def handleMessage(self):
        log.info("handling message")
        self.sendMessage(self.data)

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
