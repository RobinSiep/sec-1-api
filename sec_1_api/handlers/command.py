import logging

from pyramid.view import view_config
from socketio.namespace import BaseNamespace

from sec_1_api.lib.factories.root import RootFactory

log = logging.getLogger(__name__)


from socketio.namespace import BaseNamespace
class CommandNameSpace(BaseNamespace):
	def initialize(self):
		print("INIT")

	def on_command(self):
		print('kutjes')



def command(request):
    from socketio import socketio_manage
    log.info('fuck')
    socketio_manage(request.environ, 
    			    {'/test': CommandNameSpace},
    			    request=request)
