import logging
import os
import shutil
import zipfile

from pyramid.httpexceptions import HTTPOk, HTTPBadRequest

log = logging.getLogger(__name__)


@view_config(context=RootFactory, permission='public', renderer='json',
             request_method="POST", name="firmware")
def firmware(request):
    filename = request.POST['zip'].filename
    input_file = request.POST['zip'].file
    file_path = os.path.join('/tmp')  # moet naar firmware/versienummer
    zip_ref = zipfile.ZipFile(input_file, 'r')  # misschien a? kan niet teste
    zip_ref.extractall(file_path)
    zip_ref.close()
