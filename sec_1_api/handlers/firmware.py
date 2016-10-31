import logging
import os
import zipfile

from pyramid.view import view_config

from sec_1_api.lib.factories.root import RootFactory

log = logging.getLogger(__name__)


@view_config(context=RootFactory, permission='firmware', name='firmware',
             renderer="sec_1_api:templates/firmware.mako",
             request_method='GET')
def firmware_view(request):
    return {}


@view_config(context=RootFactory, permission='firmware', renderer='json',
             request_method="POST", name="firmware")
def firmware_upload(request):
    try:
        firmware = request.POST['firmware']
    except:
        raise HTTPBadRequest(json_body={"firmware": "No file uploaded"})

    file_path = '/../firmware/{}'.format(firmware.filename[:-4])
    input_file = firmware.file

    with zipfile.ZipFile(input_file, 'r') as zip_ref:
        zip_ref.extractall(file_path)
