import datetime
import logging
import uuid


from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy_utils import UUIDType

from sec_1_api.models.meta import Base, DBSession as session

log = logging.getLogger(__name__)


class Firmware(Base):
    __tablename__ = 'firmware'

    id = Column(
        UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    firmware_version = Column(String(250), unique=True)
    user_id = Column(UUIDType, ForeignKey('user.id'))
    date_created = Column(
        DateTime(timezone=True), default=datetime.datetime.utcnow())


def get_latest_firmware():
    return session.query(Firmware).order_by(
        Firmware.date_created.desc()).first()
