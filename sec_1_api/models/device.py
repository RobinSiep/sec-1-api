import logging
import uuid

from sqlalchemy import Column, String, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from sec_1_api.models.meta import UUID, Base, DBSession as session

log = logging.getLogger(__name__)


device_user = Table('device_user', Base.metadata,
                    Column('link_id', UUID, ForeignKey('device.link_id')),
                    Column('user_id', UUID, ForeignKey('user.id'))
                    )


class Device(Base):
    __tablename__ = 'device'

    link_id = Column(
        UUID, primary_key=True, default=uuid.uuid4)
    secret_identifier = Column(String(250), unique=True)
    name = Column(String(250))
    on = Column(Boolean())
    pattern = Column(String(100))

    users = relationship('User', secondary=device_user,
                         backref='devices')


def get_device_by_link_id(link_id):
    return session.query(Device).filter(Device.link_id == link_id).one()


def get_device_by_secret_identifier(secret_identifier):
    return session.query(Device).filter(
        Device.secret_identifier == secret_identifier).one()


def get_devices_by_user_id(user_id):
    return session.query(Device).filter(Device.users.any(
        id=user_id)).all()
