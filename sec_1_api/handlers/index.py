import logging

from pyramid.view import view_config
from pyramid.response import FileResponse
from sec_1_api.lib.factories.root import RootFactory
import os

log = logging.getLogger(__name__)


here = os.path.dirname(os.path.abspath(__file__))


@view_config(context=RootFactory, permission='public', renderer='json',
             request_method='GET')
def root_view(request):
    return {"sec-1-api": "0.1"}


@view_config(context=RootFactory, permission='public', renderer='json',
             request_method='GET', name='firmware')
def firmware(request):
    return {"version": "0.2"}


@view_config(context=RootFactory, permission='public',
             request_method='GET', name='download')
def firmware_download(request):
    response = FileResponse(os.path.join(here, 'testfile.txt'), request=request)
    response.headers['Content-Type'] = 'application/download'
    response.headers['Content-Disposition'] = 'attachement; filename="firmware.txt"'
    return response
