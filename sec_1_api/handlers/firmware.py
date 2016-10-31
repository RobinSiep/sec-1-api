import logging
import os
import re
import zipfile

from packaging import version
from pyramid.httpexceptions import (HTTPBadRequest, HTTPInternalServerError,
                                    HTTPCreated)
from pyramid.view import view_config

from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.models import commit, persist, rollback
from sec_1_api.models.firmware import Firmware, get_latest_firmware

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

    if firmware.filename[-4:] != ".zip":
        raise HTTPBadRequest(json_body={"firmware": "Invalid filetype"})

    filename = firmware.filename[:-4]

    version_regex = re.compile("^([0-9.])+$")
    if not version_regex.match(filename):
        raise HTTPBadRequest(json_body={
            "firmware": "Filename not a version number"
        })

    latest_firmware = get_latest_firmware()

    if (version.parse(filename) <= version.parse(
            latest_firmware.firmware_version)):
        raise HTTPBadRequest(json_body={
            "firmware": "A later firmware version was found"
        })

    new_firmware = Firmware(firmware_version=filename,
                            user_id=request.user.id)

    try:
        persist(new_firmware)
    except:
        log.critical("Something went wrong saving the firmware", exc_info=True)
        rollback()
        raise HTTPInternalServerError
    finally:
        commit()

    root_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = '/../firmware/{}'.format(firmware.filename[:-4])
    path = os.path.join("{}{}".format(root_dir, file_path))
    input_file = firmware.file

    with zipfile.ZipFile(input_file, 'r') as zip_ref:
        zip_ref.extractall(path)

    raise HTTPCreated
