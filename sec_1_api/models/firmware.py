import datetime
import logging
import uuid


from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from sec_1_api.models.meta import Base, UUID, DBSession as session

log = logging.getLogger(__name__)


class Firmware(Base):
    __tablename__ = 'firmware'

    id = Column(
        UUID, primary_key=True, default=uuid.uuid4)
    firmware_version = Column(String(250), unique=True)
    user_id = Column(UUID, ForeignKey('user.id'))
    date_created = Column(
        DateTime(timezone=True), default=datetime.datetime.utcnow())

    uploader = relationship('User', lazy="joined", uselist=False)


def get_latest_firmware():
    return session.query(Firmware).order_by(
        Firmware.date_created.desc()).first()


def get_firmware():
    return session.query(Firmware).order_by(
        Firmware.date_created.desc())
