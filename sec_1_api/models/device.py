import logging
import uuid

from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy_utils import UUIDType

from sec_1_api.models.meta import Base, DBSession as session

log = logging.getLogger(__name__)


device_user = Table('device_user', Base.metadata,
                    Column('link_id', UUIDType, ForeignKey('device.link_id')),
                    Column('user_id', UUIDType, ForeignKey('user.id'))
                    )


class Device(Base):
    __tablename__ = 'device'

    link_id = Column(
        UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    secret_identifier = Column(String(250), unique=True)
    on = Column(Boolean(default=False))
    pattern = Column(String(100))


def get_device_by_link_id(link_id):
    return session.query(Device).filter(Device.link_id == link_id).one()


def get_device_by_secret_identifier(secret_identifier):
    return session.query(Device).filter(Device.secret_identifier == secret_identifier).one()
